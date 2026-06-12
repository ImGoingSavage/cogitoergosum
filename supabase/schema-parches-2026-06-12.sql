-- =============================================================
-- CogitoErgoSum — Parches 2026-06-12 (auditoría):
--   (1) FK de invitaciones.usado_por: borrar_mi_cuenta() fallaba con
--       error de FK para cualquier usuario que canjeó un código (§0.1).
--   (2) uid único en events: idempotencia del outbox (los reintentos
--       duplicados se ignorarán con on_conflict=uid).
-- Ejecutar UNA VEZ en el SQL Editor. Idempotente: re-ejecutar no daña.
-- =============================================================

alter table public.invitaciones
  drop constraint if exists invitaciones_usado_por_fkey;
alter table public.invitaciones
  add constraint invitaciones_usado_por_fkey
    foreign key (usado_por) references auth.users (id) on delete set null;

alter table public.events add column if not exists uid text unique;
