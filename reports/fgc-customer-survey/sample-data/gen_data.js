// Runs the Foster BI Toolkit Sample Data Maker (copied into ../vendor, with a golf survey added) in Node.
// Writes the TMDL script (plain calculated tables) and a JSON preview of every table's rows.
const fs = require('fs'), path = require('path'), vm = require('vm');
const V = path.join(__dirname, '..', 'vendor');
const src = ['sd_names.js', 'sd_core.js', 'sd_ind.js'].map(f => fs.readFileSync(path.join(V, f), 'utf8')).join('\n');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(src + '\n;this.SD = SD; this.SD_IND = SD_IND;', ctx);
const { SD, SD_IND } = ctx;
SD.names = 'madeup';
const seed = 2026;
const args = { start_date: SD.serial(2024, 11, 1), end_date: SD.serial(2026, 10, 31), seed, num_responses: 7200, num_respondents: 3200 };
const model = SD_IND.combine(['svygolf']);
const out = process.argv[2];
fs.writeFileSync(path.join(out, 'golf_survey_inline.tmdl'), SD.script(model, { mode: 'inline', args, measures: true, measureTable: 'new' }));
fs.writeFileSync(path.join(out, 'golf_survey_functions.tmdl'), SD.script(model, { mode: 'udf', args, measures: true, measureTable: 'new' }));
const env = { p: args, seed };
const data = {};
model.tables.forEach(t => { data[t.name] = SD.tableRows(t, env); });
fs.writeFileSync(path.join(out, 'golf_survey_rows.json'), JSON.stringify(data));
console.log(model.tables.map(t => t.name + ': ' + data[t.name].length).join('\n'));
