## How to backup data

- Using pgadmin:
    - General tab
        - Connect to the database
        - Right click on the database
        - Select backup
        - Enter a file name, include date and add .sql extension
        - Select the backup format: Tar
        - set encoding to UTF-8
        - Leave role blank
        - Click on backup
    - Data/Objects tab
        - add predata, data, postdata
        - add blobs
        - Do Not Save (Owner, Privilage, table space, unlogged table data)
    - Options tab
        - Use Column inserts
        - Use Insert commands

pg_dump -d postgresql://doadmin:XXXX@ebc-prod-readonly-do-user-12895959-0.b.db.ondigitalocean.com:
25060/wrh_organization?sslmode=require > wrh_april_28_2023_1.pgssql

Use this one, it has the -Fc option.
pg_dump -d postgresql://doadmin:XXX@ebc-prod-readonly-do-user-12895959-0.b.db.ondigitalocean.com:
25060/wrh_organization?sslmode=require -Fc > wrh_april_28_2023_1.pgssql





