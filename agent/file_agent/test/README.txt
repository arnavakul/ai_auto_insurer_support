FILE AGENT TEST DATA

Use these files to test the File Assistant Agent.

01_fir.jpg
Expected: FIR, readable=true, usable=true

02_vehicle_damage_report.jpg
Expected: VEHICLE_DAMAGE_REPORT, readable=true, usable=true

03_repair_estimate.jpg
Expected: REPAIR_ESTIMATE, readable=true, usable=true

04_invalid_random.jpg
Expected: INVALID, usable=false

05_blurry_fir.jpg
Expected: FIR or INVALID depending on model judgement; readable should ideally be false or confidence should be low.

06_damage_photo.jpg
Expected: DAMAGE_PHOTO, readable=true, usable=true

07_fir.pdf
Expected: PDF text extraction should return FIR information.

08_repair_estimate.pdf
Expected: PDF text extraction should return repair estimate information.

09_scanned_damage_report.pdf
Expected: normal PDF text extraction may return little/no text because the page is an image. This is useful for testing the limitation of the current PDF parser.

IMPORTANT:
The image files are synthetic test documents created for development. They are not real insurance or police records.
