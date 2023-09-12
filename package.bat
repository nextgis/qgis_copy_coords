mkdir copy_coords
mkdir copy_coords\icons
mkdir copy_coords\i18n
xcopy *.py copy_coords
xcopy *.ui copy_coords
xcopy README.md copy_coords
xcopy LICENSE copy_coords
xcopy metadata.txt copy_coords
xcopy icons\cursor.png copy_coords\icons\cursor.png
xcopy i18n\copy_coords_ru.ts copy_coords\i18n\copy_coords_ru.ts
lrelease copy_coords\i18n\copy_coords_ru.ts
del copy_coords\i18n\copy_coords_ru.ts
zip -r copy_coords.zip copy_coords
del /s /q copy_coords
rmdir /s /q copy_coords