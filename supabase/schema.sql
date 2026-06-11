-- =============================================================
-- CogitoErgoSum — esquema de Supabase (HANDOFFCES §5.2 C.1)
-- Ejecutar UNA VEZ en el SQL Editor del proyecto:
--   supabase.com → tu proyecto → SQL Editor → pegar todo → Run
-- =============================================================

-- Event log append-only (§3.4): los historiales se UNEN, nunca colisionan
create table public.events (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  device_id text not null,
  ts timestamptz not null default now(),
  tipo text not null,        -- 'sesion'|'piso'|'unidad'|'examen'|'insignia'|'migracion'
  payload jsonb not null
);
create index events_user_ts on public.events (user_id, ts);

-- Snapshot del estado derivado (arranque rápido en dispositivo nuevo)
create table public.snapshots (
  user_id uuid primary key references auth.users (id) on delete cascade,
  actualizado timestamptz not null default now(),
  estado jsonb not null
);

-- Keep-alive: una fila que el cron de GitHub toca con un select trivial
create table public.keepalive ( id int primary key, nota text );
insert into public.keepalive (id, nota) values (1, 'cron keep-alive');

alter table public.events enable row level security;
alter table public.snapshots enable row level security;
alter table public.keepalive enable row level security;

create policy "events: leer propios" on public.events
  for select using (auth.uid() = user_id);
create policy "events: insertar propios" on public.events
  for insert with check (auth.uid() = user_id);
-- append-only deliberado: SIN políticas de update/delete para el cliente

create policy "snapshot: leer propio" on public.snapshots
  for select using (auth.uid() = user_id);
create policy "snapshot: crear propio" on public.snapshots
  for insert with check (auth.uid() = user_id);
create policy "snapshot: actualizar propio" on public.snapshots
  for update using (auth.uid() = user_id);

create policy "keepalive: lectura anonima" on public.keepalive
  for select using (true);

-- Borrar cuenta en 2 clics (Constitución §0.1): el cliente no puede tocar
-- auth.users, así que se expone una RPC security definer que borra al
-- propio usuario; events y snapshots caen en cascada.
create or replace function public.borrar_mi_cuenta()
returns void language plpgsql security definer set search_path = public as $$
begin
  delete from auth.users where id = auth.uid();
end $$;
revoke all on function public.borrar_mi_cuenta() from public;
grant execute on function public.borrar_mi_cuenta() to authenticated;
