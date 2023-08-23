mkdir copy_coords\i18n
xcopy i18n copy_coords\i18n
xcopy *.py copy_coords
xcopy *.ui copy_coords
xcopy README.md copy_coords
xcopy metadata.txt copy_coords
zip -r copy_coords.zip copy_coords
del /Q copy_coords
rd copy_coords