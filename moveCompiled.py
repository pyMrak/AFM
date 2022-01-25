import shutil
#import AFM
from libs import globalPaths


#ver = AFM.version.plit('_'[0]).strip('ver')
compiled = r'dist\AFM'
target = "AFM_build1"#globalPaths.path.download + 'AFM'

shutil.move(compiled, target)

for folder in ["Fonts", "Graphic", "QC", "Settings", "Templates"]:
    shutil.copytree(folder, target+'/'+folder, dirs_exist_ok=True)

for folder in ["dist", "build"]:
    shutil.rmtree(folder)

