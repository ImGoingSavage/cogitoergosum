-- =============================================================
-- CogitoErgoSum — Fase D: "El claustro" (HANDOFFCES §2.4)
-- Ejecutar UNA VEZ en el SQL Editor (después de schema.sql):
--   supabase.com → tu proyecto → SQL Editor → pegar todo → Run
--
-- Principios (Constitución §0): inspiración, no dominancia.
-- Lo ÚNICO visible de un amigo es su vitrina (avatar, sellos,
-- rachas, moraleja compartida opt-in). Sin actividad en tiempo
-- real, sin puntajes, sin rankings. Única interacción: el
-- reconocimiento ❧ (uno por sello por amigo, no acumulable).
-- =============================================================

-- Perfil-vitrina: lo que el dueño decide publicar para sus amigos
create table public.perfiles (
  user_id uuid primary key references auth.users (id) on delete cascade,
  username text not null unique check (char_length(username) between 3 and 24),
  vitrina jsonb not null default '{}'::jsonb,
  actualizado timestamptz not null default now()
);

-- Amistades simétricas (una fila por vínculo)
create table public.amistades (
  id bigint generated always as identity primary key,
  user_a uuid not null references auth.users (id) on delete cascade,
  user_b uuid not null references auth.users (id) on delete cascade,
  creado timestamptz not null default now(),
  unique (user_a, user_b),
  check (user_a <> user_b)
);

-- Invitaciones por código (un código = un amigo; sin sugerencias algorítmicas)
create table public.invitaciones (
  codigo text primary key check (char_length(codigo) between 8 and 24),
  de_user uuid not null references auth.users (id) on delete cascade,
  creado timestamptz not null default now(),
  usado_por uuid references auth.users (id)
);

-- Reconocimiento ❧: la única interacción. Único por (de, para, sello):
-- jamás se convierte en contador de popularidad.
create table public.reconocimientos (
  id bigint generated always as identity primary key,
  de_user uuid not null references auth.users (id) on delete cascade,
  para_user uuid not null references auth.users (id) on delete cascade,
  insignia_id text not null,
  creado timestamptz not null default now(),
  visto boolean not null default false,
  unique (de_user, para_user, insignia_id),
  check (de_user <> para_user)
);

-- ¿Existe vínculo entre dos usuarios? (security definer para usarla en RLS)
create or replace function public.son_amigos(u1 uuid, u2 uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from amistades
    where (user_a = u1 and user_b = u2) or (user_a = u2 and user_b = u1)
  );
$$;
grant execute on function public.son_amigos(uuid, uuid) to authenticated;

alter table public.perfiles enable row level security;
alter table public.amistades enable row level security;
alter table public.invitaciones enable row level security;
alter table public.reconocimientos enable row level security;

-- Perfiles: el dueño escribe; lo leen el dueño y SUS amigos (nadie más)
create policy "perfil: leer propio o de amigo" on public.perfiles
  for select using (auth.uid() = user_id or public.son_amigos(auth.uid(), user_id));
create policy "perfil: crear propio" on public.perfiles
  for insert with check (auth.uid() = user_id);
create policy "perfil: actualizar propio" on public.perfiles
  for update using (auth.uid() = user_id);

-- Amistades: visibles y disolubles por cualquiera de los dos (2 clics, §0.1).
-- SIN política de insert: el vínculo solo nace vía canjear_invitacion().
create policy "amistad: ver propias" on public.amistades
  for select using (auth.uid() in (user_a, user_b));
create policy "amistad: disolver propias" on public.amistades
  for delete using (auth.uid() in (user_a, user_b));

-- Invitaciones: cada quien gestiona las suyas
create policy "invitacion: crear propia" on public.invitaciones
  for insert with check (auth.uid() = de_user);
create policy "invitacion: ver propias" on public.invitaciones
  for select using (auth.uid() = de_user);
create policy "invitacion: revocar propia" on public.invitaciones
  for delete using (auth.uid() = de_user);

-- Reconocimientos: solo entre amigos; el receptor puede marcarlos vistos
create policy "reconocer: solo a amigos" on public.reconocimientos
  for insert with check (
    auth.uid() = de_user and public.son_amigos(de_user, para_user)
  );
create policy "reconocimiento: ver propios" on public.reconocimientos
  for select using (auth.uid() in (de_user, para_user));
create policy "reconocimiento: marcar visto" on public.reconocimientos
  for update using (auth.uid() = para_user) with check (auth.uid() = para_user);

-- Canje de invitación (security definer: crea el vínculo y quema el código)
create or replace function public.canjear_invitacion(codigo_entrada text)
returns text language plpgsql security definer set search_path = public as $$
declare
  inv record;
  nombre text;
begin
  select * into inv from invitaciones
    where codigo = upper(trim(codigo_entrada)) and usado_por is null;
  if not found then
    raise exception 'Código inválido o ya usado';
  end if;
  if inv.de_user = auth.uid() then
    raise exception 'Ese código es tuyo: compártelo con un amigo';
  end if;
  if son_amigos(auth.uid(), inv.de_user) then
    raise exception 'Ya existe el vínculo con esa persona';
  end if;
  insert into amistades (user_a, user_b) values (inv.de_user, auth.uid());
  update invitaciones set usado_por = auth.uid() where codigo = inv.codigo;
  select username into nombre from perfiles where user_id = inv.de_user;
  return coalesce(nombre, 'tu nuevo colega');
end $$;
revoke all on function public.canjear_invitacion(text) from public;
grant execute on function public.canjear_invitacion(text) to authenticated;
