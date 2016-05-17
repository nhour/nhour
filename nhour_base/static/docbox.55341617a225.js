function DocFetcher(models) {
    this.models = this.objectsByPrimaryKey(models);
}

DocFetcher.prototype.objectsByPrimaryKey = function(objects) {
    var byPrimaryKey = {};
    for (var i = 0; i < objects.length; i++) {
        var object = objects[i]
        byPrimaryKey[object.pk] = object;
    }
    return byPrimaryKey;
}

DocFetcher.prototype.getDocumentation = function(primaryKey) {
    return this.models[primaryKey].fields.description;
}

function DocBox(models, dropdown, docbox) {
    var docFetcher = new DocFetcher(models)
    dropdown.click(function(event) {
        selected = dropdown.children("option:selected")
        docbox.text(docFetcher.getDocumentation(selected.val()));
    });
}