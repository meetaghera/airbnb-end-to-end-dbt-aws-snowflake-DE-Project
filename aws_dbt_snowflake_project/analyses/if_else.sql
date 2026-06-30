{% set flag = 1 %}

SELECT * FROM {{ ref('bronze_hosts') }}
{% if flag == 1 %}
    WHERE RESPONSE_RATE = 95
{% else %}
    WHERE RESPONSE_RATE = 100   
{% endif %}
