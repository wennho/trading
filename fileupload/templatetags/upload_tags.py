from django import template

register = template.Library()

@register.simple_tag
def upload_js():
    return """
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
<tbody class="template-upload fade">
    <tr>
        <td rowspan=2>
            <span class="preview"></span>
        </td>
        <td>
            <div class="form-group">
                <input id="id_{%=file.name%}-title" name="{%=file.name%}-title" placeholder="Item Name" type="text" class="form-control" />
            </div>
            {% if (file.error) { %}
                <div><span class="label label-important">{%=locale.fileupload.error%}</span> {%=file.error%}</div>
            {% } %}
        </td>
        <td>
            <div class="form-group">
                $ <input id="id_{%=file.name%}-price" name="{%=file.name%}-price" placeholder="Price" type="text" class="form-control price" size=8/>
            </div>
        </td>
        <td rowspan=2>
            {% if (!o.files.error && !i && !o.options.autoUpload) { %}
                <button class="btn btn-primary start">
                    <i class="glyphicon glyphicon-upload"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}
            {% if (!i) { %}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>{%=locale.fileupload.cancel%}</span>
                </button>
            {% } %}
        </td>
    </tr>
    <tr>
        <td colspan=2 class="notopborder">
            <div class="form-group">
                <textarea id="id_{%=file.name%}-description" name="{%=file.name%}-description" placeholder="Description (optional)" class="form-control" />
            </div>
        </td>
    </tr>
    </tbody>
{% } %}
</script>

"""






