mkdir copy_coords
mkdir copy_coords\icons
mkdir copy_coords\i18n
xcopy *.py copy_coords
xcopy *.ui copy_coords
xcopy README.md copy_coords
xcopy LICENSE copy_coords
xcopy metadata.txt copy_coords
xcopy icons\cursor.png copy_coords\icons\cursor.png
lrelease copy_coords\i18n\about_base_ru.ts
zip -r copy_coords.zip copy_coords
del /Q copy_coords
rd copy_coords