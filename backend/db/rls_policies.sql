-- Apply after the Alembic migration on Supabase-managed Postgres. FastAPI also
-- enforces project membership; these policies add defense in depth to Supabase
-- Auth and the private Storage bucket.

-- Drop the original public helpers/policies safely when upgrading from the
-- initial scaffold, then recreate this file's policies idempotently.
drop policy if exists "members read projects" on public.projects;
drop policy if exists "owners create projects" on public.projects;
drop policy if exists "owners update projects" on public.projects;
drop policy if exists "owners delete projects" on public.projects;
drop policy if exists "members read project memberships" on public.project_members;
drop policy if exists "owners manage project memberships" on public.project_members;
drop policy if exists "members access rooms" on public.rooms;
drop policy if exists "members read project assets" on public.assets;
drop policy if exists "members create own project assets" on public.assets;
drop policy if exists "members update own project assets" on public.assets;
drop policy if exists "members delete own project assets" on public.assets;
drop policy if exists "members access briefs" on public.briefs;
drop policy if exists "members access agent messages" on public.agent_messages;
drop policy if exists "members access generation jobs" on public.generation_jobs;
drop policy if exists "members read project results" on public.results;
drop policy if exists "members select project results" on public.results;
drop policy if exists "project members read private MAYA assets" on storage.objects;
drop policy if exists "project members upload private MAYA assets" on storage.objects;
drop policy if exists "project members delete private MAYA assets" on storage.objects;
drop function if exists public.maya_is_project_member(uuid);
drop function if exists public.maya_is_project_owner(uuid);

-- These SECURITY DEFINER helpers prevent recursive membership policies. Keep
-- them out of exposed schemas, pin an empty search_path, qualify all names,
-- and grant execution only to authenticated users.
create schema if not exists maya_private;
revoke all on schema maya_private from public;
grant usage on schema maya_private to authenticated;

create or replace function maya_private.is_project_member(target_project uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select (select auth.uid()) is not null and (
    exists (
      select 1
      from public.projects as p
      where p.id = target_project and p.owner_id = (select auth.uid())::text
    )
    or exists (
      select 1
      from public.project_members as pm
      where pm.project_id = target_project and pm.user_id = (select auth.uid())::text
    )
  );
$$;

create or replace function maya_private.is_project_owner(target_project uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select (select auth.uid()) is not null and exists (
    select 1
    from public.projects as p
    where p.id = target_project and p.owner_id = (select auth.uid())::text
  );
$$;

revoke execute on function maya_private.is_project_member(uuid) from public, anon, service_role;
revoke execute on function maya_private.is_project_owner(uuid) from public, anon, service_role;
grant execute on function maya_private.is_project_member(uuid) to authenticated;
grant execute on function maya_private.is_project_owner(uuid) to authenticated;

alter table public.projects enable row level security;
alter table public.project_members enable row level security;
alter table public.rooms enable row level security;
alter table public.assets enable row level security;
alter table public.briefs enable row level security;
alter table public.agent_messages enable row level security;
alter table public.generation_jobs enable row level security;
alter table public.results enable row level security;

create policy "members read projects" on public.projects for select to authenticated
  using ((select maya_private.is_project_member(id)));
create policy "owners create projects" on public.projects for insert to authenticated
  with check (owner_id = (select auth.uid())::text);
create policy "owners update projects" on public.projects for update to authenticated
  using ((select maya_private.is_project_owner(id)))
  with check ((select maya_private.is_project_owner(id)));
create policy "owners delete projects" on public.projects for delete to authenticated
  using ((select maya_private.is_project_owner(id)));

create policy "members read project memberships" on public.project_members for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "owners manage project memberships" on public.project_members for all to authenticated
  using ((select maya_private.is_project_owner(project_id)))
  with check ((select maya_private.is_project_owner(project_id)));

create policy "members read rooms" on public.rooms for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "members create rooms" on public.rooms for insert to authenticated
  with check ((select maya_private.is_project_member(project_id)));
create policy "members update rooms" on public.rooms for update to authenticated
  using ((select maya_private.is_project_member(project_id)))
  with check ((select maya_private.is_project_member(project_id)));
create policy "members delete rooms" on public.rooms for delete to authenticated
  using ((select maya_private.is_project_member(project_id)));

create policy "members read project assets" on public.assets for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "members create own project assets" on public.assets for insert to authenticated
  with check (
    owner_id = (select auth.uid())::text
    and (select maya_private.is_project_member(project_id))
  );
create policy "members update own project assets" on public.assets for update to authenticated
  using (owner_id = (select auth.uid())::text and (select maya_private.is_project_member(project_id)))
  with check (owner_id = (select auth.uid())::text and (select maya_private.is_project_member(project_id)));
create policy "members delete own project assets" on public.assets for delete to authenticated
  using (owner_id = (select auth.uid())::text and (select maya_private.is_project_member(project_id)));

create policy "members read briefs" on public.briefs for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "members create own briefs" on public.briefs for insert to authenticated
  with check (
    created_by = (select auth.uid())::text
    and (select maya_private.is_project_member(project_id))
  );
create policy "creators update own briefs" on public.briefs for update to authenticated
  using (created_by = (select auth.uid())::text and (select maya_private.is_project_member(project_id)))
  with check (created_by = (select auth.uid())::text and (select maya_private.is_project_member(project_id)));
create policy "creators delete own briefs" on public.briefs for delete to authenticated
  using (created_by = (select auth.uid())::text and (select maya_private.is_project_member(project_id)));

create policy "members read agent messages" on public.agent_messages for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "users create own agent messages" on public.agent_messages for insert to authenticated
  with check (
    user_id = (select auth.uid())::text
    and (select maya_private.is_project_member(project_id))
  );

create policy "members read generation jobs" on public.generation_jobs for select to authenticated
  using ((select maya_private.is_project_member(project_id)));
create policy "members create generation jobs" on public.generation_jobs for insert to authenticated
  with check (
    requested_by = (select auth.uid())::text
    and (select maya_private.is_project_member(project_id))
  );
create policy "requesters or owners update generation jobs" on public.generation_jobs for update to authenticated
  using (
    (select maya_private.is_project_member(project_id))
    and (
      requested_by = (select auth.uid())::text
      or (select maya_private.is_project_owner(project_id))
    )
  )
  with check (
    (select maya_private.is_project_member(project_id))
    and (
      requested_by = (select auth.uid())::text
      or (select maya_private.is_project_owner(project_id))
    )
  );

create policy "members read project results" on public.results for select to authenticated
  using (exists (
    select 1 from public.generation_jobs as j
    where j.id = results.job_id and (select maya_private.is_project_member(j.project_id))
  ));
create policy "members select project results" on public.results for update to authenticated
  using (exists (
    select 1 from public.generation_jobs as j
    where j.id = results.job_id and (select maya_private.is_project_member(j.project_id))
  ))
  with check (
    (selected_by = (select auth.uid())::text or selected_by is null)
    and exists (
      select 1 from public.generation_jobs as j
      where j.id = results.job_id and (select maya_private.is_project_member(j.project_id))
    )
  );

insert into storage.buckets (id, name, public)
values ('maya-assets', 'maya-assets', false)
on conflict (id) do update set public = false;

create policy "project members read private MAYA assets" on storage.objects for select to authenticated
  using (
    bucket_id = 'maya-assets'
    and case
      when (storage.foldername(name))[1] ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
      then (select maya_private.is_project_member(((storage.foldername(name))[1])::uuid))
      else false
    end
  );
create policy "project members upload private MAYA assets" on storage.objects for insert to authenticated
  with check (
    bucket_id = 'maya-assets'
    and owner_id = (select auth.uid())::text
    and case
      when (storage.foldername(name))[1] ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
      then (select maya_private.is_project_member(((storage.foldername(name))[1])::uuid))
      else false
    end
  );
create policy "project members delete own private MAYA assets" on storage.objects for delete to authenticated
  using (
    bucket_id = 'maya-assets'
    and owner_id = (select auth.uid())::text
    and case
      when (storage.foldername(name))[1] ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
      then (select maya_private.is_project_member(((storage.foldername(name))[1])::uuid))
      else false
    end
  );
