from psycopg import sql


def get_views_query():
    query = sql.SQL(
        """
    WITH
    performance_parser AS (
        SELECT
            CASE
                WHEN COALESCE(h.currentsheet, '') = '' OR h.currentsheet LIKE '%% %%' OR currentsheet LIKE '%%/null'
                THEN
                    SPLIT_PART(
                        CASE SPLIT_PART(http_request_uri, '/', 2)
                            WHEN 'views' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            WHEN 't' THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                            WHEN 'trusted' THEN SPLIT_PART(http_request_uri, '/', 5) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 6), '?', 1)
                            WHEN 'vizql' THEN
                                CASE SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 3)
                                    WHEN 'w' THEN
                                        CASE
                                            WHEN LEFT(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), 12) = '/vizql/w/ds:'
                                            THEN REPLACE(SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 4), 'ds:', '')
                                            ELSE SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 4)
                                        END ||
                                        CASE
                                            WHEN SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 6) = 'null'
                                            THEN ''
                                            ELSE '/' || SPLIT_PART(REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'), '/', 6)
                                        END
                                    WHEN 'authoring' THEN ''
                                    ELSE ''
                                END
                            WHEN 'askData' THEN SPLIT_PART(http_request_uri, '/', 3)
                            WHEN 'authoringNewWorkbook' THEN SPLIT_PART(http_request_uri, '/', 4)
                            WHEN 'authoring' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            WHEN 'startAskData' THEN SPLIT_PART(SPLIT_PART(http_request_uri, '/', 3), '?', 1)
                            WHEN 'offline_views' THEN SPLIT_PART(http_request_uri, '/', 3) || '/' || SPLIT_PART(SPLIT_PART(http_request_uri, '/', 4), '?', 1)
                            ELSE NULL
                        END,
                        '.',
                        1
                    )
                ELSE
                    CASE WHEN ( LEFT(currentsheet, 3) = 'ds:' OR LEFT(http_request_uri, 22) = '/authoringNewWorkbook/' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:')
                    THEN
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
                    ELSE
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 1)
                        || '/' ||
                        SPLIT_PART(REPLACE(h.currentsheet, 'ds:', ''), '/', 2)
                    END
            END AS item_repository_url,
            CASE
                WHEN currentsheet LIKE 'ds:%%' OR LEFT(http_request_uri, 12) = '/vizql/w/ds:' OR LEFT(http_request_uri, 9) = '/askData/'
                THEN 'Data Source'
                WHEN http_request_uri LIKE '/authoringNewWorkbook/%%'
                OR 
                SPLIT_PART(
                    REPLACE(http_request_uri, ('/vizql/t/' || COALESCE(s.url_namespace, '')), '/vizql'),
                    '/',
                    6
                ) = 'null'
                AND
                currentsheet NOT LIKE '%%/%%'
                THEN 'Workbook'
                ELSE 'View'
            END AS item_type,
            h.site_id,
            date(h.created_at) event_date,
            sum(EXTRACT(EPOCH FROM (h.completed_at - h.created_at))) AS duration_secs_total_nbr,
            count(*) as event_count_total_nbr
        FROM http_requests AS h
        LEFT JOIN sites AS s ON h.site_id = s.id
        WHERE action = 'bootstrapSession'
        AND LEFT(CAST(h.status AS TEXT), 1) = '2'
        group by 1,2,3,4
    ),
    performance_summary AS (
        SELECT
        REPLACE(item_repository_url, '/', '/sheets/') AS view_repository_url,
        site_id,

        sum(duration_secs_total_nbr) / 
        NULLIF(sum(event_count_total_nbr), 0) AS duration_secs_avg_total_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '7 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '7 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_7d_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '28 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '28 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_28d_nbr,

        sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '90 days' THEN duration_secs_total_nbr ELSE 0 END) / 
        NULLIF(sum(CASE WHEN event_date >= CURRENT_DATE - INTERVAL '90 days' THEN event_count_total_nbr ELSE 0 END), 0) AS duration_secs_avg_90d_nbr
        FROM performance_parser pp
        WHERE item_type = 'View'
        GROUP BY 1, 2
    ),
    total_usage as (
      select
        date(he.created_at) event_date,
        v.id view_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_views hv 
        on he.hist_view_id = hv.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join views v
        on v.id = hv.view_id and v.site_id = hs.site_id
      group by 1,2,3,4
    ),
    usage_summary AS (
        SELECT
            view_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'workbook'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          v.name object_name,
          v.luid object_luid,
          v.updated_at object_updated_at,
          su.name object_owner_id,
          su.friendly_name object_owner_name,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,

          ps.duration_secs_avg_total_nbr,
          ps.duration_secs_avg_7d_nbr,
          ps.duration_secs_avg_28d_nbr,
          ps.duration_secs_avg_90d_nbr,

          us.unique_users_total_nbr,
          us.unique_users_7d_nbr,
          us.unique_users_28d_nbr,
          us.unique_users_90d_nbr,

          us.event_count_total_nbr,
          us.event_count_7d_nbr,
          us.event_count_28d_nbr,
          us.event_count_90d_nbr,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from views v
        join sites s
          on s.id = v.site_id
        left outer join users u
          on u.id = v.owner_id
         and u.site_id = v.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = v.workbook_id
         and pp.site_id = v.site_id
        left outer join performance_summary ps
          on ps.view_repository_url = v.repository_url
         and ps.site_id = v.site_id
        left outer join usage_summary us
          on us.view_id = v.id
         and us.site_id = v.site_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
    CASE
    WHEN {sort_column} IS NULL THEN 1
    ELSE 0
    END,
    {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )

    return query


def get_workbooks_query():
    query = sql.SQL(
        """
    WITH
    total_usage as (
      select
        date(he.created_at) event_date,
        v.workbook_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_views hv 
        on he.hist_view_id = hv.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join views v
        on v.id = hv.view_id and v.site_id = hs.site_id
      group by 1,2,3,4
    ),
    usage_summary AS (
        SELECT
            workbook_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'workbook'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          w.name object_name,
          w.luid object_luid,
          w.size object_size,
          w.updated_at object_updated_at,
          su.name object_owner_id,
          su.friendly_name object_owner_name,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.unique_users_total_nbr,
          us.unique_users_7d_nbr,
          us.unique_users_28d_nbr,
          us.unique_users_90d_nbr,

          us.event_count_total_nbr,
          us.event_count_7d_nbr,
          us.event_count_28d_nbr,
          us.event_count_90d_nbr,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from workbooks w
        join sites s
          on s.id = w.site_id
        left outer join users u
          on u.id = w.owner_id
         and u.site_id = w.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = w.id
         and pp.site_id = w.site_id
        left outer join usage_summary us
          on us.workbook_id = w.id
         and us.site_id = w.site_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )

    return query


def get_datasources_query():
    return sql.SQL(
        """
    WITH
    total_usage as (
      select
        date(he.created_at) event_date,
        d.id datasource_id,
        hs.site_id,
        he.hist_actor_user_id,
        count(*) event_count
      from historical_events he
      join hist_datasources hd
        on he.hist_datasource_id = hd.id
      join hist_sites hs
        on hs.id = he.hist_target_site_id
      join datasources d
        on d.id = hd.datasource_id and d.site_id = hs.site_id
      group by 1,2,3,4
    ),
    usage_summary AS (
        SELECT
            datasource_id,
            site_id,
            max(event_date) last_event_date,

            COUNT(DISTINCT hist_actor_user_id) AS unique_users_total_nbr,
            sum(event_count) AS event_count_total_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '7 days' then hist_actor_user_id end) AS unique_users_7d_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '28 days' then hist_actor_user_id end) AS unique_users_28d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,

            COUNT(DISTINCT case when event_date >= CURRENT_DATE - INTERVAL '90 days' then hist_actor_user_id end) AS unique_users_90d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'datasource'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          d.name object_name,
          d.luid object_luid,
          d.size object_size,
          d.db_class object_db_class,
          d.connectable object_connectable,
          d.updated_at object_updated_at,
          w.name parent_workbook_name,
          w.luid parent_workbook_luid,
          su.name object_owner_id,
          su.friendly_name object_owner_name,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.unique_users_total_nbr,
          us.unique_users_7d_nbr,
          us.unique_users_28d_nbr,
          us.unique_users_90d_nbr,

          us.event_count_total_nbr,
          us.event_count_7d_nbr,
          us.event_count_28d_nbr,
          us.event_count_90d_nbr,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from datasources d
        join sites s
          on s.id = d.site_id
        left outer join workbooks w
          on w.id = d.parent_workbook_id
         and w.site_id = d.site_id
        left outer join users u
          on u.id = d.owner_id
         and u.site_id = d.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = d.id
         and pp.site_id = d.site_id
        left outer join usage_summary us
          on us.datasource_id = d.id
         and us.site_id = d.site_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )


def get_extract_refreshes_query():
    return sql.SQL(
        """
    WITH
    total_usage as (
      select
        date(bj.created_at) event_date,
        bj.task_id,
        bj.site_id,
        count(*) event_count
      from background_jobs bj
      join tasks t
        on t.id = bj.task_id
       and t.site_id = bj.site_id
      where t.type in ('RefreshExtractTask', 'IncrementExtractTask')
        and bj.finish_code = 0
      group by 1,2,3
    ),
    usage_summary AS (
        SELECT
            task_id,
            site_id,
            max(event_date) last_event_date,
            sum(event_count) AS event_count_total_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                pc.content_type,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type in ('datasource', 'workbook')
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                ph.content_type,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            content_type,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          t.luid object_luid,
          t.type object_type,
          CASE
              WHEN t.state = 0 THEN 'Active'
              WHEN t.state = 1 THEN 'Suspended'
              WHEN t.state = 2 THEN 'Disabled'
              ELSE 'Unknown'
          END object_state,
          t.updated_at object_updated_at,
          CASE
              WHEN sch.schedule_type = 0 THEN 'Hourly'
              WHEN sch.schedule_type = 1 THEN 'Daily'
              WHEN sch.schedule_type = 2 THEN 'Weekly'
              WHEN sch.schedule_type = 3 THEN 'Monthly'
              ELSE 'Unknown'
          END schedule_type,
          su.name object_owner_id,
          su.friendly_name object_owner_name,
          coalesce(w.name, d.name) content_name,
          t.obj_type content_type,
          csu.name content_owner_id,
          csu.friendly_name content_owner_name,
          pp.full_project_path content_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.event_count_total_nbr,
          us.event_count_7d_nbr,
          us.event_count_28d_nbr,
          us.event_count_90d_nbr,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from tasks t
        join sites s
          on s.id = t.site_id
        left outer join users u
          on u.id = t.creator_id
         and u.site_id = t.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join usage_summary us
          on us.task_id = t.id
         and us.site_id = t.site_id
        left outer join project_path pp
          on pp.content_id = t.obj_id
         and pp.content_type = lower(t.obj_type)
         and pp.site_id = t.site_id
        left outer join workbooks w
          on w.id = t.obj_id
         and t.obj_type = 'Workbook'
         and w.site_id = t.site_id
        left outer join datasources d
          on d.id = t.obj_id
         and t.obj_type = 'Datasource'
         and d.site_id = t.site_id
        left outer join users cu
          on cu.id = coalesce(w.owner_id, d.owner_id)
         and cu.site_id = t.site_id
        left outer join system_users csu
          on csu.id = cu.system_user_id
        left outer join schedules sch
          on sch.id = t.schedule_id
        where t.type in ('RefreshExtractTask', 'IncrementExtractTask')
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )


def get_subscriptions_query():
    return sql.SQL(
        """
    WITH
    total_usage as (
      select
        date(bj.created_at) event_date,
        bj.task_id,
        bj.site_id,
        count(*) event_count
      from background_jobs bj
      join tasks t
        on t.id = bj.task_id
       and t.site_id = bj.site_id
      where t.type = 'SingleSubscriptionTask'
        and bj.finish_code = 0
      group by 1,2,3
    ),
    usage_summary AS (
        SELECT
            task_id,
            site_id,
            max(event_date) last_event_date,
            sum(event_count) AS event_count_total_nbr,
            sum(case when event_date >= current_date - interval '7 days' then event_count else 0 end) AS event_count_7d_nbr,
            sum(case when event_date >= current_date - interval '28 days' then event_count else 0 end) AS event_count_28d_nbr,
            sum(case when event_date >= current_date - interval '90 days' then event_count else 0 end) AS event_count_90d_nbr
        from total_usage
        group by 1,2
    ),
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'workbook'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          t.luid object_luid,
          t.type object_type,
          CASE
              WHEN t.state = 0 THEN 'Active'
              WHEN t.state = 1 THEN 'Suspended'
              WHEN t.state = 2 THEN 'Disabled'
              ELSE 'Unknown'
          END object_state,
          CASE
              WHEN sch.schedule_type = 0 THEN 'Hourly'
              WHEN sch.schedule_type = 1 THEN 'Daily'
              WHEN sch.schedule_type = 2 THEN 'Weekly'
              WHEN sch.schedule_type = 3 THEN 'Monthly'
              ELSE 'Unknown'
          END schedule_type,
          t.updated_at object_updated_at,
          su.name object_owner_id,
          su.friendly_name object_owner_name,
          su.email object_owner_email,
          coalesce(w.name, v.name) content_name,
          sub.target_type content_type,
          csu.name content_owner_id,
          csu.friendly_name content_owner_name,
          pp.full_project_path content_full_project_path,
          s.name site_name,
          s.luid site_luid,

          us.event_count_total_nbr,
          us.event_count_7d_nbr,
          us.event_count_28d_nbr,
          us.event_count_90d_nbr,
          
          us.last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from subscriptions sub
        join sites s
          on s.id = sub.site_id
        join schedules sch
          on sch.id = sub.schedule_id
        left outer join tasks t
          on t.obj_id = sub.id
         and t.site_id = sub.site_id
        left outer join users u
          on u.id = t.creator_id
         and u.site_id = t.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join usage_summary us
          on us.task_id = t.id
         and us.site_id = t.site_id
        left outer join workbooks w
          on w.id = sub.target_id
         and w.site_id = sub.site_id
        left outer join views v
          on v.id = sub.target_id
         and v.site_id = sub.site_id
        left outer join workbooks vw
          on vw.id = sub.target_id
         and vw.site_id = sub.site_id
        left outer join project_path pp
          on pp.content_id = coalesce(w.id, vw.id)
         and pp.site_id = sub.site_id
        left outer join users cu
          on cu.id = coalesce(w.owner_id, v.owner_id)
         and cu.site_id = t.site_id
        left outer join system_users csu
          on csu.id = cu.system_user_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )


def get_data_alerts_query():
    return sql.SQL(
        """
    with
    total_usage as (
    select
    date(created_at) event_date,
    SPLIT_PART(SPLIT_PART(he.details, 'dataAlertId:', 2), ',', 1)::int AS data_alert_id,
    SPLIT_PART(SPLIT_PART(he.details, 'siteId:', 2), ',', 1)::int AS site_id,
    SPLIT_PART(SPLIT_PART(he.details, 'userId:', 2), ',', 1)::int user_id,
    count(*) event_count
    from historical_events he
    where he.historical_event_type_id = 236
    group by 1,2,3,4
    ),
    usage_summary as (
    select
        data_alert_id,
        site_id,
        max(event_date) last_event_date,
        count(distinct user_id) unique_users_total_nbr,
        sum(event_count) event_count_total_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '7 days' then user_id end) unique_users_7d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) event_count_7d_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '28 days' then user_id end) unique_users_28d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) event_count_28d_nbr,
                    
        count(distinct case when event_date >= CURRENT_DATE - INTERVAL '90 days' then user_id end) unique_users_90d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '90 days' then event_count else 0 end) event_count_90d_nbr
    from total_usage
    group by 1,2
    ),
    final as (
    select
    CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
    da.luid object_luid,
    da.title object_name,
    da.updated_at object_updated_at,
    su.name object_owner_id,
    su.friendly_name object_owner_name,
    su.email object_owner_email,
    s.luid site_luid,
    s.name site_name,
    summ.last_event_date,
    summ.unique_users_total_nbr,
    summ.event_count_total_nbr,
    summ.unique_users_7d_nbr,
    summ.event_count_7d_nbr,
    summ.unique_users_28d_nbr,
    summ.event_count_28d_nbr,
    summ.unique_users_90d_nbr,
    summ.event_count_90d_nbr
    from data_alerts da
    join sites s
    on s.id = da.site_id
    left join users u
    on u.id = da.creator_id
    and u.site_id = da.site_id
    left join system_users su
    on su.id = u.system_user_id
    left join usage_summary summ
    on summ.data_alert_id = da.id
    and summ.site_id = da.site_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )


def get_customized_views_query():
    return sql.SQL("""
    WITH
    project_path AS (
        WITH RECURSIVE project_hierarchy AS (
            SELECT
                pc.site_id,
                pc.content_id,
                p.id AS project_id,
                p.name AS project_name,
                p.parent_project_id,
                1 AS level,
                p.name::character varying AS path
            FROM projects_contents pc
            JOIN projects p ON pc.project_id = p.id
            WHERE pc.content_type = 'workbook'
            UNION ALL
            SELECT
                ph.site_id,
                ph.content_id,
                p.id,
                p.name,
                p.parent_project_id,
                ph.level + 1,
                (p.name || ' >> ' || ph.path)::character varying
            FROM project_hierarchy ph
            JOIN projects p ON ph.parent_project_id = p.id
            AND ph.site_id = p.site_id
        )
        SELECT
            site_id,
            content_id,
            path AS full_project_path
        FROM project_hierarchy
        WHERE parent_project_id IS NULL
    ),
    final as (
        select
          v.name object_name,
          v.luid object_luid,
          su.name object_owner_id,
          v.modified_at object_updated_at,
          su.friendly_name object_owner_name,
          su.email object_owner_email,
          pp.full_project_path object_full_project_path,
          s.name site_name,
          s.luid site_luid,
          date(v.accessed_at) last_event_date,
          CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at
        from customized_views v
        join sites s
          on s.id = v.site_id
        join views vv
          on vv.id = v.view_id
         and vv.site_id = v.site_id
        left outer join users u
          on u.id = vv.owner_id
         and u.site_id = vv.site_id
        left outer join system_users su
          on su.id = u.system_user_id
        left outer join project_path pp
          on pp.content_id = vv.workbook_id
         and pp.site_id = vv.site_id
    )
    select * from final
    WHERE (%(owner_id)s::text IS NULL OR object_owner_id = %(owner_id)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    ORDER BY
    CASE
    WHEN {sort_column} IS NULL THEN 1
    ELSE 0
    END,
    {sort_column} {sort_direction}
    LIMIT %(limit)s
    """)


def get_users_query():
    return sql.SQL(
        """
    with
    total_usage as (
    select
    date(he.created_at) event_date,
    et.action_type,
    hs.site_id,
    hu.user_id,
    count(*) event_count
    from historical_events he
    join historical_event_types et
      on et.type_id = he.historical_event_type_id
    join hist_sites hs
      on hs.id = he.hist_actor_site_id
    join hist_users hu
      on hu.id = he.hist_actor_user_id
    group by 1,2,3,4
    ),
    usage_summary as (
    select
        user_id,
        site_id,
        max(event_date) last_event_date,
        sum(event_count) event_count_total_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '7 days' then 1 else 0 end) event_count_7d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '28 days' then 1 else 0 end) event_count_28d_nbr,
        sum(case when event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) event_count_90d_nbr,

        sum(case when action_type = 'Access' then event_count else 0 end) access_event_count_total_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) access_event_count_7d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) access_event_count_28d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) access_event_count_90d_nbr,

        sum(case when action_type = 'Create' then event_count else 0 end) create_event_count_total_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) create_event_count_7d_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) create_event_count_28d_nbr,
        sum(case when action_type = 'Create' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) create_event_count_90d_nbr,

        sum(case when action_type = 'Publish' then event_count else 0 end) publish_event_count_total_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '7 days' then event_count else 0 end) publish_event_count_7d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '28 days' then event_count else 0 end) publish_event_count_28d_nbr,
        sum(case when action_type = 'Access' and event_date >= CURRENT_DATE - INTERVAL '90 days' then 1 else 0 end) publish_event_count_90d_nbr
    from total_usage
    group by 1,2
    ),
    final as (
    select
    CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AS snapshot_at,
    u.luid object_luid,
    su.name object_name,
    su.friendly_name object_full_name,
    su.email object_email,
    REGEXP_REPLACE(sr.display_name, '[\\s()]', '', 'g') site_role_name,
    s.luid site_luid,
    s.name site_name,
    summ.last_event_date,

    summ.event_count_total_nbr,
    summ.event_count_7d_nbr,
    summ.event_count_28d_nbr,
    summ.event_count_90d_nbr,

    summ.access_event_count_total_nbr,
    summ.access_event_count_7d_nbr,
    summ.access_event_count_28d_nbr,
    summ.access_event_count_90d_nbr,

    summ.create_event_count_total_nbr,
    summ.create_event_count_7d_nbr,
    summ.create_event_count_28d_nbr,
    summ.create_event_count_90d_nbr,

    summ.publish_event_count_total_nbr,
    summ.publish_event_count_7d_nbr,
    summ.publish_event_count_28d_nbr,
    summ.publish_event_count_90d_nbr
    from system_users su
    join users u
      on u.system_user_id = su.id
    join site_roles sr
      on sr.id = u.site_role_id
    join sites s
      on s.id = u.site_id
    left join usage_summary summ
      on summ.user_id = u.id
     and summ.site_id = u.site_id
    )
    select * from final
    WHERE (%(user_name)s::text IS NULL OR object_name = %(user_name)s::text)
    AND (%(site_name)s::text IS NULL OR site_name = %(site_name)s::text)
    AND (%(exclude_unlicensed)s::boolean IS FALSE OR site_role_name != 'Unlicensed')
    ORDER BY
        CASE
            WHEN {sort_column} IS NULL THEN 1
            ELSE 0
        END,
        {sort_column} {sort_direction}
    LIMIT %(limit)s
    """
    )
