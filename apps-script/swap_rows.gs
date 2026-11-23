/**
 * SpearPoint 90 Day Plan: swap rows.
 * When "Swap for alternative" or "Not Relevant" is chosen and an alternative is picked in
 * "Swap with", the alternative is inserted as a new row directly below, in that section's
 * format. Clearing the pick (or changing the decision) removes that row again.
 * Runs as a simple onEdit trigger on the 90 Day Plan tab only. No outside access.
 */
var PLAN_TAB = 'SpearPoint 90 Day Plan Recommendations';
var SWAP_HEADER = 'Swap with (alternative)';
var SWAP_DECISIONS = ['Swap for alternative', 'Not Relevant'];

// 1-based columns for each section type
var LAYOUTS = {
  page:  { id: 1,  status: 11, dec: 12, next: 13, notes: 14, swap: 15, swapped: 16 },
  tech:  { id: 1,  status: 11, dec: 12, next: 13, notes: 14, swap: 15, swapped: 16 },
  blog:  { id: 12, dec: 14, next: 15, notes: 16, swap: 17, swapped: 18 },
  guest: { id: 13, dec: 16, next: 17, notes: 18, swap: 19, swapped: 20 }
};

function onEdit(e) {
  if (!e || !e.range) return;
  var sh = e.range.getSheet();
  if (sh.getName() !== PLAN_TAB) return;
  if (e.range.getNumRows() !== 1 || e.range.getNumColumns() !== 1) return;
  var row = e.range.getRow(), col = e.range.getColumn();
  var sec = findSection_(sh, row);
  if (!sec || row <= sec.headerRow) return;
  var L = LAYOUTS[sec.type];
  if (col !== L.swap && col !== L.dec) return;
  var lock = LockService.getDocumentLock();
  lock.waitLock(15000);
  try { syncRow_(sh, row, sec.type); } finally { lock.releaseLock(); }
}

/** Find the header row above `row` and the section type it belongs to. */
function findSection_(sh, row) {
  var vals = sh.getRange(1, 1, row, 20).getDisplayValues();
  for (var r = row - 1; r >= 0; r--) {
    var v = vals[r];
    if (v[14] === SWAP_HEADER) return { headerRow: r + 1, type: v[2] === 'Page URL' ? 'page' : 'tech' };
    if (v[16] === SWAP_HEADER) return { headerRow: r + 1, type: 'blog' };
    if (v[18] === SWAP_HEADER) return { headerRow: r + 1, type: 'guest' };
    if (v[0] === 'ID' && v[1] === 'Plan bucket') return null; // alternatives section
  }
  return null;
}

function syncRow_(sh, row, type) {
  var L = LAYOUTS[type];
  var data = sh.getRange(row, 1, 1, 20).getDisplayValues()[0];
  var origId = data[L.id - 1];
  if (!origId) return;
  var decision = data[L.dec - 1];
  var pick = data[L.swap - 1];
  var marker = 'Swapped in for ' + origId;
  var wanted = pick && SWAP_DECISIONS.indexOf(decision) !== -1;
  var alt = wanted ? findAlt_(sh, pick) : null;

  // Is there already an inserted row directly below for this task?
  var below = row + 1;
  var hasRow = below <= sh.getMaxRows() && sh.getRange(below, L.notes).getDisplayValue() === marker;
  if (hasRow) {
    var currentAltId = sh.getRange(below, L.id).getDisplayValue();
    if (wanted && alt && currentAltId === alt[0]) return; // already correct
    sh.deleteRow(below);
  }
  if (!wanted || !alt) return;

  sh.insertRowAfter(row);
  var nr = row + 1;
  // Same dropdowns and formulas as the original row
  sh.getRange(row, 1, 1, 20).copyTo(sh.getRange(nr, 1, 1, 20), SpreadsheetApp.CopyPasteType.PASTE_DATA_VALIDATION, false);
  sh.getRange(row, L.next).copyTo(sh.getRange(nr, L.next), SpreadsheetApp.CopyPasteType.PASTE_FORMULA, false);
  sh.getRange(row, L.swapped).copyTo(sh.getRange(nr, L.swapped), SpreadsheetApp.CopyPasteType.PASTE_FORMULA, false);

  // alt columns: 0 ID, 1 bucket, 2 task, 3 why, 4 page, 5 from, 6 effort
  var hours = parseHours_(alt[6]);
  var put = {};
  if (type === 'page') {
    put = { 1: alt[0], 2: "'" + data[1], 3: alt[4], 4: hours, 5: alt[1], 6: alt[2], 7: alt[3], 9: alt[5], 10: data[9], 11: 'Not Started' };
  } else if (type === 'tech') {
    put = { 1: alt[0], 2: "'" + data[1], 3: alt[2], 4: hours, 5: alt[3], 6: alt[4], 7: alt[5], 11: 'Not Started' };
  } else if (type === 'blog') {
    put = { 1: "'" + data[0], 2: data[1], 4: alt[4], 7: 'Suggested topic: ' + alt[2] + '. ' + alt[3], 8: data[7], 11: 'Not Started', 12: alt[0], 13: alt[5] };
  } else if (type === 'guest') {
    put = { 1: data[0], 2: data[1], 4: alt[4], 8: '1 link', 9: alt[2] + '. ' + alt[3], 11: 'Not Started', 13: alt[0], 14: alt[3] };
  }
  put[L.notes] = marker;
  Object.keys(put).forEach(function (c) { sh.getRange(nr, Number(c)).setValue(put[c]); });

  extendRules_(sh, row);
}

/** Look up an alternative by its pick label (column N of the alternatives section). */
function findAlt_(sh, pick) {
  var vals = sh.getDataRange().getDisplayValues();
  for (var r = 0; r < vals.length; r++) {
    if (/^A\d+$/.test(vals[r][0]) && vals[r][13] === pick) return vals[r];
  }
  return null;
}

function parseHours_(effort) {
  var m = String(effort).match(/^([\d.]+)\s*hr/);
  return m ? Number(m[1]) : '';
}

/** A row inserted under the last row of a range is outside it; stretch those highlight rules by one row. */
function extendRules_(sh, origRow) {
  var rules = sh.getConditionalFormatRules();
  var changed = false;
  var out = rules.map(function (rule) {
    var hit = false;
    var ranges = rule.getRanges().map(function (rg) {
      if (rg.getLastRow() === origRow) {
        hit = true;
        return sh.getRange(rg.getRow(), rg.getColumn(), rg.getNumRows() + 1, rg.getNumColumns());
      }
      return rg;
    });
    if (!hit) return rule;
    changed = true;
    return rule.copy().setRanges(ranges).build();
  });
  if (changed) sh.setConditionalFormatRules(out);
}
