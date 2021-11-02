define(['backbone', 'utils/class'], function (Backbone, UtilClass) {
    var LocalStorage = UtilClass.extend({
        initialize: function () {
            
        },
        isDict: function(v) {
            return typeof v==='object' && v!==null && !(v instanceof Array) && !(v instanceof Date);
        },
        clear: function () {
            localStorage.clear();
        },
        isStorageSupported: function () {
            return (typeof(Storage) !== 'undefined');
        },
        setItem: function (key, value) {
            if (this.isStorageSupported()) {
                if (this.isDict(value)) {
                    localStorage.setItem(key, JSON.stringify(value));
                } else {
                    localStorage.setItem(key, value);
                }
            }
        },
        setItemDict: function (itemName, key, value) {
            var item = this.getItem(itemName);
            if (item === null) {
                // Create new dict
                this.setItem(itemName, {
                    key: value
                });
            } else {
                if (this.isDict(item)) {
                    item[key] = value;
                } else {
                    item = {
                        key: value
                    };
                }
                this.setItem(itemName, item);
            }
        },
        getItemDict: function (itemName, key) {
            var item = this.getItem(itemName);
            if (this.isDict(item)) {
                if (item.hasOwnProperty(key)) {
                    return item[key];
                } else {
                    return null;
                }
            }
            return null;
        },
        getItem: function (key) {
            if (this.isStorageSupported()) {
                try {
                    return JSON.parse(localStorage.getItem(key));
                } catch (e) {
                    return localStorage.getItem(key);
                }
            }
            return null;
        },
        hashItem: function (itemString) {
            return itemString.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
        }
    });

    return LocalStorage;
});
