{% macro bronze_health_check() %}

{%- set bronze_models = [] -%}
{%- for node in graph.nodes.values() -%}
    {%- if node.resource_type == 'model' and node.config.materialized == 'incremental' and 'bronze' in node.schema -%}
        {%- do bronze_models.append(node) -%}
    {%- endif -%}
{%- endfor -%}

{% if bronze_models | length == 0 %}
    {{ log("No incremental bronze models found in the graph.", info=true) }}
{% else %}

{% for model in bronze_models %}
SELECT
    '{{ model.name }}' AS model_name,
    COUNT(*) AS total_rows,
    MAX(CREATED_AT) AS latest_load_timestamp,
    DATEDIFF('hour', MAX(CREATED_AT), CURRENT_TIMESTAMP()) AS hours_since_last_load
FROM {{ ref(model.name) }}
{% if not loop.last %}
UNION ALL
{% endif %}
{% endfor %}
ORDER BY model_name

{% endif %}

{% endmacro %}
