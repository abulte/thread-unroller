---
title: "{{ thread.title }}"
---
{% for tweet in thread.tweets -%}

{%- if loop.index == 1 -%}
# {{ thread.title }}
{%- endif %}

{{ tweet }}

{% if not loop.last -%}
---
{%- endif %}

{% endfor %}
