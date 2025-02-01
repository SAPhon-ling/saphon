import sys, os

from python.saphon.io import *

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# from io import *
if len(sys.argv) < 3:
   print('write.py SAPHON_DIR HTML_DIR')
   sys.exit(1)

saphonDir, htmlDir, ipatable = sys.argv[1:4]

#saphonData = saphon.io.readSaphonFiles(saphonDir)
saphonData = readSaphonYAMLFiles(saphonDir, ipatable)

generationModules = [__import__(m) for m in (
  'write_inventories',
  'write_phonemes',
  'write_lists',
  'write_saphon_php',
  'write_lang_xml')]

localizationModules = [__import__(m) for m in
  ('en', 'es', 'pt')]

# Create directories
os.makedirs(htmlDir, exist_ok=True)
for locMod in localizationModules:
  os.makedirs(htmlDir + '/' + locMod.metalang_code, exist_ok=True)
  os.makedirs(htmlDir + '/' + locMod.metalang_code + '/inv', exist_ok=True)

# Create HTML files 
for genMod in generationModules:
  if hasattr(genMod, 'write'):
    genMod.write(saphonData, htmlDir)
  if hasattr(genMod, 'writeLocal'):
    for locMod in localizationModules:
      genMod.writeLocal(saphonData, htmlDir, locMod)
