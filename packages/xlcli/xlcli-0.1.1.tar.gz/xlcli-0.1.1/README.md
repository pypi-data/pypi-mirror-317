# xlcli

simple Excel Viewer in Terminal

## Usage

To see information about an Excel file, use the following command:

```bash
xlcli info <file>
```

this will display the number of sheets, the first sheet in the file, and all sheet names that exist.

To print out the contents of an Excel sheet, use the following command:

```bash
xlcli print <file> [--sheet <sheet>]
```
