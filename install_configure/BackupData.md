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

