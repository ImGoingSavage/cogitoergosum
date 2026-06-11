-- =============================================================
-- CogitoErgoSum — "Pensar juntos" (HANDOFFCES §2.4 punto 15)
-- Aprobado por el usuario 2026-06-11: el problema se SORTEA del
-- pool común (curados que ninguno trabajó). Sin ganador.
-- Ejecutar UNA VEZ en el SQL Editor (después de schema-fase-d.sql).
-- =============================================================

create table public.pensar_juntos (
  id bigint generated always as identity primary key,
  user_a uuid not null references auth.users (id) on delete cascade, -- proponente
  user_b uuid not null references auth.users (id) on delete cascade, -- invitado
  candidatos jsonb not null,   -- ids curados no trabajados del proponente (barajados)
  problem_id int,              -- null hasta que el invitado acepta y sortea
  estado text not null default 'propuesta' check (estado in ('propuesta', 'activa')),
  creado timestamptz not null default now(),
  check (user_a <> user_b)
);

-- Entregas: una por participante. {desconstruccion, moraleja, disparador, fecha}
create table public.pj_entregas (
  pj_id bigint not null references public.pensar_juntos (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  payload jsonb not null,
  creado timestamptz not null default now(),
  primary key (pj_id, user_id)
);

-- ¿Ya entregué yo en este pensar-juntos? (security definer: evita la
-- recursión de una política que se consulta a sí misma)
create or replace function public.tengo_entrega(pj bigint)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from pj_entregas where pj_id = pj and user_id = auth.uid()
  );
$$;
grant execute on function public.tengo_entrega(bigint) to authenticated;

alter table public.pensar_juntos enable row level security;
alter table public.pj_entregas enable row level security;

-- pensar_juntos: lo ven y lo retiran ambos; solo se propone a un AMIGO;
-- solo el invitado acepta (fija problem_id y estado)
create policy "pj: ver propios" on public.pensar_juntos
  for select using (auth.uid() in (user_a, user_b));
create policy "pj: proponer a un amigo" on public.pensar_juntos
  for insert with check (auth.uid() = user_a and public.son_amigos(user_a, user_b));
create policy "pj: aceptar" on public.pensar_juntos
  for update using (auth.uid() = user_b and estado = 'propuesta')
  with check (auth.uid() = user_b);
create policy "pj: retirar" on public.pensar_juntos
  for delete using (auth.uid() in (user_a, user_b));

-- Entregas — la política que materializa el "struggle first":
-- insertas SOLO la tuya (y solo si participas); LEES la del otro
-- únicamente cuando la tuya ya existe. Sin excepciones de UI.
create policy "entrega: crear propia" on public.pj_entregas
  for insert with check (
    auth.uid() = user_id
    and exists (
      select 1 from pensar_juntos pj
      where pj.id = pj_id and auth.uid() in (pj.user_a, pj.user_b)
    )
  );
create policy "entrega: struggle first" on public.pj_entregas
  for select using (user_id = auth.uid() or public.tengo_entrega(pj_id));
