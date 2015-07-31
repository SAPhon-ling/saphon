from collections import *

# Read in IPA sounds and properties.
# TODO: Error checking on sound info.
soundInfo = OrderedDict()
for line in open('data/ipa_table.txt'):
  if ':' not in line: continue
  position, sounds = re.split(': *', line, 1)
  for sound in re.split(' +', sounds):
    soundInfo[sound] = position

# Predicates on phonemes.
def isVoiced(sound): return soundInfo[sound][3] == 'v'
def isLabialized(sound): return 'ʷ' in sound
def isPalatalized(sound): return 'ʲ' in sound
def isAffricate(sound):
  return soundMap[sound][1] in "aesvp" \
     and soundMap[sound][2] in "AoRP"
def isEjective(sound): return '\'' in sound

# Quantifiers.
def indic(x): return not not x
def count(seq, pred): return sum(pred(x) for x in seq)

def NONE(seq, pred=indic): return count(seq, pred) == 0
def ANY (seq, pred=indic): return count(seq, pred) >= 1
def MANY(seq, pred=indic): return count(seq, pred) >= 2
def ALL (seq, pred=indic): return count(seq, pred) == len(seq)

# Write a table labeled `name` with `sounds`, using `optimizeLayout`
# to improve the initial layout derived from soundInfo, using
# `formatLabel` to format labels and `formatSounds` to format lists
# of sounds, and using `write` to write.

def writeTable(name, sounds, optimizeLayout, formatLabel, formatSounds, write):

  # Create initial layout
  layout = defaultdict(list)
  for sound in sounds:
    info = soundInfo[sound]
    layout[info[1], info[2]].append(sound)

  # Improve layouts, get relevant table rows/columns.
  rowLabels, colLabels = layoutOptimizer(layout)

  # Write out layout
  write('<div class=field><table class=inv>\n')

  for i in ['?'] + rowLabels.keys():
    write('<tr>')
    if i == '?': # top-left cell
      write('<td class=key>')
      write(formatLabel(name))
      write('</td>')
    else: # row header
      write('<td class=header>')
      write(formatLabel(rowLabels(i)))
      write('</td>')

    for j in colLabels.keys():
      if i == '?': # column header
        write('<td class=header>')
        write(formatLabel(colLabels(j)))
        write('</td>')
      else: # body cells
        write('<td>')
        write(formatSounds(layout[i,j]))
        write('</td>')
    write('</tr>\n')

  write('</table></div>\n')

# Write a field labeled `name` with `nonsounds`, using `formatLabel`
# to format labels and `formatSounds` to format lists of sounds, and
# using `writeField` to write.

def writeNonsounds(name, nonsounds, formatLabel, formatNonsounds, writeField):
  writeField(formatLabel(name), formatNonsounds(nonsounds))

#  if( table) {
#    write( "<div class=field>\n")
#    write( "<div class=key>" 
#      ++ Xlt(loc, "suprasegmental")) 
#      ++ ":</div>\n")
#    write( "<div class=value>")
#    write( assembleTrans( ss_))
#    write( "</div></div>\n")
#  } else if( !ss_.isEmpty) {
#    write( "<div class=field><div class=key>" 
#      ++ Xlt(loc, "suprasegmental")) 
#      ++ "</div><div class=value>")
#    write( cap( ss_.map( xlt(loc, _)).mkString( ", ")))
#    write( "</div></div>\n")
#  }

def writeLocal(saphonData, htmlDir, loc):
  metalang = loc.metalang_code

  inventoryHead = """
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <link rel="stylesheet" type="text/css" href="../../inv.css" />
  </head>
  <body>
  """

  # Create a file for our own use that contains all inventories.
  foMaster = open(htmlDir+'/'+metalang+'/inv/master.html', 'w')
  foMaster.write(inventoryHead)

  for lang in saphonData.lang_:
    fo = open(htmlDir+'/'+metalang+'/inv/'+lang.nameComp+'.html', 'w')
    fo.write(inventoryHead)

    # For writing to master and individual inventories simultaneously.
    def write(s):
      foMaster.write(s)
      fo.write(s)

    def writeField(fieldName, fieldValue):
      write('<div class=field><div class=key>')
      write(Xlt(loc, fieldName))
      write('</div><div class=value>')
      write(fieldValue)
      write('</div></div>\n')

    write('<div class=entry>\n')
    write('<h1>%s</h1>\n' % lang.name)

    if lang.nameAlt_:
      writeField('other names', '; '.join(lang.nameAlt_))

    if lang.iso_:
      writeField('language code', ', '.join(lang.iso_))

    writeField('location', '; '.join(geo.toLatLonString for geo in lang.geo_))

    writeField('family', lang.familyStr)

    writeTable(
      'consonants',
      [s for s in sounds if soundInfo[s][0] == 'c'],
      lambda layout: optimizeConsonantLayout(layout, lump),
      lambda label: Xlt(loc, label),
      lambda sounds: '&nbsp'.join(sounds),
      write)

    writeTable(
      'vowels',
      [s for s in sounds if soundInfo[s][0] == 'v'],
      lambda layout: optimizeVowelLayout(layout, lump),
      lambda label: Xlt(loc, label),
      lambda sounds: '&nbsp'.join(sounds),
      write)

    writeNonsounds(
      'suprasegmentals',
      [s for s in sounds if soundInfo[s][0] == 's'],
      lambda label: Xlt(loc, label),
      lambda sounds: ', '.join(xlt(loc, sounds)).capitalize(),
      writeField)
      
    if lang.bib_:
      bibStr = ''.join('<p>'+bib+'</p>\n' for bib in lang.bib_)
      writeField('bibliography', bibStr)

    if lang.note_:
      noteStr = ''.join('<p>'+note+'</p>\n' for note in lang.note_)
      writeField('notes', noteStr)
        
    write('</div>\n') # Close class=entry.

    fo.write('</body>\n')
    fo.close()

  foMaster.write('</body>\n')
  foMaster.close()
