openerp.disable_decimal = function (instance) {
    var _t = instance.web._t;
    console.log("Hollaaaaaaaaaa");
    //instance.web.views.add('disable_decimal_points', 'instance.web.disable_decimal.RemovePoints');

    instance.web.TranslationDataBase = instance.web.TranslationDataBase.extend({
        init: function() {
            this.db = {};
            this.parameters = {"date_format": '%m/%d/%Y',
                            "time_format": '%H:%M:%S',
                            "grouping": [],
                            "decimal_point": ".",
                            "thousands_sep": ",",
                            "view_decimal": true};
        }
    });

    var normalize_format = function (format) {
        return Date.normalizeFormat(instance.web.strip_raw_chars(format));
    };

    instance.web.format_value = function(value, descriptor, value_if_empty) {

        // If NaN value, display as with a `false` (empty cell)
        if (typeof value === 'number' && isNaN(value)) {
            value = false;
        }
        //noinspection FallthroughInSwitchStatementJS
        switch (value) {
            case '':
                if (descriptor.type === 'char') {
                    return '';
                }
                console.warn('Field', descriptor, 'had an empty string as value, treating as false...');
            case false:
            case Infinity:
            case -Infinity:
                return value_if_empty === undefined ?  '' : value_if_empty;
        }
        var l10n = _t.database.parameters;
        switch (descriptor.widget || descriptor.type || (descriptor.field && descriptor.field.type)) {
            case 'id':
                return value.toString();
            case 'integer':
                return instance.web.insert_thousand_seps(
                    _.str.sprintf('%d', value));
            case 'float':
                if (l10n.view_decimal){
                    var digits = descriptor.digits ? descriptor.digits : [69,2];
                    digits = typeof digits === "string" ? py.eval(digits) : digits;
                    var precision = digits[1];
                    var formatted = _.str.sprintf('%.' + precision + 'f', value).split('.');
                    formatted[0] = instance.web.insert_thousand_seps(formatted[0]);
                    return formatted.join(l10n.decimal_point);
               } else {
                   return instance.web.insert_thousand_seps(
                            _.str.sprintf('%d', value));
               }
            case 'float_time':
                var pattern = '%02d:%02d';
                if (value < 0) {
                    value = Math.abs(value);
                    pattern = '-' + pattern;
                }
                var hour = Math.floor(value);
                var min = Math.round((value % 1) * 60);
                if (min == 60){
                    min = 0;
                    hour = hour + 1;
                }
                return _.str.sprintf(pattern, hour, min);
            case 'many2one':
                // name_get value format
                return value[1] ? value[1].split("\n")[0] : value[1];
            case 'one2many':
            case 'many2many':
                if (typeof value === 'string') {
                    return value;
                }
                return _.str.sprintf(_t("(%d records)"), value.length);
            case 'datetime':
                if (typeof(value) == "string")
                    value = instance.web.auto_str_to_date(value);

                return value.toString(normalize_format(l10n.date_format)
                            + ' ' + normalize_format(l10n.time_format));
            case 'date':
                if (typeof(value) == "string")
                    value = instance.web.auto_str_to_date(value);
                return value.toString(normalize_format(l10n.date_format));
            case 'time':
                if (typeof(value) == "string")
                    value = instance.web.auto_str_to_date(value);
                return value.toString(normalize_format(l10n.time_format));
            case 'selection': case 'statusbar':
                // Each choice is [value, label]
                if(_.isArray(value)) {
                     value = value[0]
                }
                var result = _(descriptor.selection).detect(function (choice) {
                    return choice[0] === value;
                });
                if (result) { return result[1]; }
                return;
            default:
                return value;
        }
    }
};
