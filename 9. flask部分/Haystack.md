# Haystack

## 1.什么是Haystack

Haystack是django的开源全文搜索框架(全文检索不同于特定字段的模糊查询，使用全文检索的效率更高 )，该框架支持**Solr**,**Elasticsearch**,**Whoosh**, ***Xapian*搜索引擎它是一个可插拔的后端（很像Django的数据库层），所以几乎你所有写的代码都可以在不同搜索引擎之间便捷切换

## 2.安装

```python
pip install django-haystack
```

## 3.配置

###添加Haystack到`INSTALLED_APPS`

跟大多数Django的应用一样，你应该在你的设置文件(通常是`settings.py`)添加Haystack到`INSTALLED_APPS`.  示例： 

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # 添加
    'haystack',

    # 你的app
    'blog',
]
```

###修改`settings.py`

在你的`settings.py`中，你需要添加一个设置来指示站点配置文件正在使用的后端，以及其它的后端设置。  `HAYSTACK——CONNECTIONS`是必需的设置，并且应该至少是以下的一种： 

#### Solr示例

```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
```

#### Elasticsearch示例

```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
```

#### Whoosh示例

```python
#需要设置PATH到你的Whoosh索引的文件系统位置
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
```

#### Xapian示例

```python
#首先安装Xapian后端（http://github.com/notanumber/xapian-haystack/tree/master）
#需要设置PATH到你的Xapian索引的文件系统位置。
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index'),
    },
}
```

## 4.处理数据

### 创建`SearchIndexes` 

`SearchIndexes`对象是Haystack决定那些数据应该放入索引和处理流数据的方式。你可以把它们看作是Django的`Models`或`Forms`，它们是基于字段和数据操作/存储的。

你通常为你期望索引的每一个`Model`都创建一个唯一的`SearchIndex`。虽然你可以在不同的model中重复使用相同的`SearchIndex`，只要你小心的做并且字段名很规范。

为了建立`SearchIndex`，所有的都是`indexes.SearchIndex`和`indexe.Indexable`的子类。定义要存储数据的字段，定义`get_model`方法。

我们会在下面创建和`Note`模型对应的`NoteIndex`。这个代码通常在`search_indexes.py`中。尽管这不是必须的。这使得Haystack能自动的检测到它。`NoteIndex`应该看起来像：

 ```python
import datetime
from haystack import indexes
from myapp.models import Note

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
 ```

每个`SerachIndex`需要有一个（仅有一个）一个字段`document=True`.这个指示着Haystack和搜索引擎把那个字段作为主要的检索。 

```python
当你选择document=True字段时，它应该在你的SearchIndex类里面始终如一，以避免后端的混淆。一个便捷的命名是text。
在所有的样例中这个text字段名并没有什么特殊。它也可以是其他任何命名，你可以叫它pink_polka_dot也是没有关系的。只是简单便利的交做text。
```

另外，我们在`text`字段上提供了`use_template=True`。这允许我们使用一个数据模板（而不是容易出错的级联）来构建文档搜索引擎索引。你应该在模板目录下建立新的模板`search/indexes/myapp/note_text.txt`，并将下面内容放在里面。 

 ```python
{{ object.title }}
{{ object.user.get_full_name }}
{{ object.body }}
 ```

此外，我们增加了其他字段（`author`和`pub_date`）。当我们提供额外的过滤选项的时候这是很有用的。来至Haystack的多个`SearchField`类能处理大多数的数据。

一个常见的主题是允许管理员用户在未来添加内容，而不马上在网站展示，直到未来某个时间点。我们特别自定义了`index_queryset`方法来防止未来的这些项添加到索引。

## 5.设置视图

### 添加`SearchView`到你的`URLconf` 

在你的`URLconf`中添加下面一行：

 ```python
(r'^search/', include('haystack.urls')),
 ```

这会拉取Haystack的默认URLconf，它由单独指向`SearchView`实例的URLconf组成。你可以通过传递几个关键参数或者完全重新它来改变这个类的行为。

### 搜索模板

你的搜索模板(默认在`search/search.html`)将可能非常简单。下面的足够让你的搜索运行(你的`template/block`应该会不同)

 ```python
{% extends 'base.html' %}

{% block content %}
    <h2>Search</h2>

    <form method="get" action=".">
        <table>
            {{ form.as_table }}
            <tr>
                <td>&nbsp;</td>
                <td>
                    <input type="submit" value="Search">
                </td>
            </tr>
        </table>

        {% if query %}
            <h3>Results</h3>

            {% for result in page.object_list %}
                <p>
                    <a href="{{ result.object.get_absolute_url }}">{{ result.object.title }}</a>
                </p>
            {% empty %}
                <p>No results found.</p>
            {% endfor %}

            {% if page.has_previous or page.has_next %}
                <div>
                    {% if page.has_previous %}<a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">{% endif %}&laquo; Previous{% if page.has_previous %}</a>{% endif %}
                    |
                    {% if page.has_next %}<a href="?q={{ query }}&amp;page={{ page.next_page_number }}">{% endif %}Next &raquo;{% if page.has_next %}</a>{% endif %}
                </div>
            {% endif %}
        {% else %}
            {# Show some example queries to run, maybe query syntax, something else? #}
        {% endif %}
    </form>
{% endblock %}
 ```

需要注意的是`page.object_list`实际上是`SearchResult`对象的列表。这些对象返回索引的所有数据。它们可以通过`{{result.object}}`来访问。所以`{{ result.object.title}}`实际使用的是数据库中`Note`对象来访问`title`字段的。 

### 重建索引

这是最后一步，现在你已经配置好了所有的事情，是时候把数据库中的数据放入索引了。Haystack附带的一个命令行管理工具使它变得很容易。

简单的运行`./manage.py rebuild_index`。你会得到有多少模型进行了处理并放进索引的统计。

 

 

 

 

 

 



 

 

 

 

 