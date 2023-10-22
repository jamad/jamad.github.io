---
layout: post
title: Table styles
author: jamad
---

<link rel="stylesheet" type="text/css" href="/assets/css/theme.css">

>Markdown
{:.filename}
{% highlight raw %}
line to be highlighted
{% endhighlight %}


## Few more examples from kramdown [documentation](https://kramdown.gettalong.org/syntax.html#tables):

|-----------------+------------+-----------------+----------------|
| Default aligned |Left aligned| Center aligned  | Right aligned  |
|-----------------|:-----------|:---------------:|---------------:|
| First body part |Second cell | Third cell      | fourth cell    |
| Second line     |foo         | **strong**      | baz            |
| Third line      |quux        | baz             | bar            |
|-----------------+------------+-----------------+----------------|
| Second body     |            |                 |                |
| 2 line          |            |                 |                |
|=================+============+=================+================|
| Footer row      |            |                 |                |
|-----------------+------------+-----------------+----------------|

>Table header row, two table bodies and a table footer row
{:.filename}
{% highlight raw %}
|-|:-|:-:|-:
{% endhighlight %}

