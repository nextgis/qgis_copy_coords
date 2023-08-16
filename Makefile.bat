mkdir copy_coords
xcopy *.py copy_coords
xcopy *.ui copy_coords
xcopy README.md copy_coords
xcopy metadata.txt copy_coords
zip -r copy_coords.zip copy_coords
del /Q copy_coords
rd copy_coords