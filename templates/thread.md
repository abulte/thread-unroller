---
title: {% if title %}{{ title }}{% endif %}
---

{% for tweet in thread.tweets -%}

{%- if loop.index == 1 -%}
{% if title %}
# {{ title }}
{% endif %}
{%- if not title -%}#{%- endif %} {{ tweet }}
{%- else -%}
{{ tweet }}
{%- endif %}

{% if not loop.last -%}
---
{%- endif %}

{% endfor %}
