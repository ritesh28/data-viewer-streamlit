i want to build a tabular data viewer and editing/cleaning tool in python streamlit

The app should provides a rich user interface to view and analyze your data, show insightful column statistics and visualizations, and can automatically generate Pandas code as you clean and transform the data

User will upload excel or csv file to see data. User can download processed data in excel or csv format

The app has two modes when working with your data:

- Viewing mode: The viewing mode optimizes the interface for you to quickly view, filter and sort your data. This mode is great for doing initial exploration on the dataset.
- Editing mode: The Editing mode optimizes the interface for you to apply transformations, cleaning, or modifications to your dataset. As you apply these transformations in the interface, the app automatically generates the relevant Pandas code

# View mode

![view mode](./view%20mode.png)

1. The Data Summary panel shows detailed summary statistics for your overall dataset or a specific column, if one is selected.
2. You can apply any Data Filters/Sorts on the column from the header menu of the column.
3. Toggle between the Viewing or Editing mode of Data Wrangler to access the built-in data operations.
4. The Quick Insights header is where you can quickly see valuable information about each column. Depending on the datatype of the column, quick insights shows the distribution of the data or the frequency of datapoints, as well as missing and distinct values.
5. The Data Grid gives you a scrollable pane where you can view your entire dataset.

# edit mode

![edit mode](./edit%20mode.png)

1. The Operations panel is where you can search through all of Data Wrangler’s built-in data operations. The operations are organized by category.
2. The Cleaning Steps panel shows a list of all the operations that have been previously applied. It enables the user to undo specific operations or edit the most recent operation. Selecting a step will highlight the changes in the data grid and will show the generated code associated with that operation.
3. The Export Menu lets you export the code back into a Jupyter Notebook or export the data into a new file.
4. When you have an operation selected and are previewing its effects on the data, the grid is overlayed with a data diff view of the changes you made to the data.
5. The Code Preview section shows the Python and Pandas code that Data Wrangler has generated when an operation is selected. It remains empty when no operation is selected. You can edit the generated code, which results in the data grid highlighting the effects on the data.

## Modify previous steps

Each step of the generated code can be modified through the Cleaning Steps panel. First, select the step you want to modify. Then, as you make changes to the operation (either via code or the operation panel), the effects of your changes on the data are highlighted in the grid view.

## operations

| Operation                     | Description                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| Sort                          | Sort column(s) ascending or descending                                                  |
| Filter                        | Filter rows based on one or more conditions                                             |
| Calculate text length         | Create new column with values equal to the length of each string value in a text column |
| One-hot encode                | Split categorical data into a new column for each category                              |
| Change column type            | Change the data type of a column                                                        |
| Drop column                   | Delete one or more columns                                                              |
| Select column                 | Choose one or more columns to keep and delete the rest                                  |
| Rename column                 | Rename one or more columns                                                              |
| Clone column                  | Create a copy of one or more columns                                                    |
| Drop missing values           | Remove rows with missing values                                                         |
| Drop duplicate rows           | Drops all rows that have duplicate values in one or more columns                        |
| Fill missing values           | Replace cells with missing values with a new value                                      |
| Find and replace              | Replace cells with a matching pattern                                                   |
| Group by column and aggregate | Group by columns and aggregate results                                                  |
| Strip whitespace              | Remove whitespace from the beginning and end of text                                    |
| Split text                    | Split a column into several columns based on a user defined delimiter                   |
| Capitalize first character    | Converts first character to uppercase and remaining to lowercase                        |
| Convert text to lowercase     | Convert text to lowercase                                                               |
| Convert text to uppercase     | Convert text to UPPERCASE                                                               |
| Scale min/max values          | Scale a numerical column between a minimum and maximum value                            |
| Round                         | Rounds numbers to the specified number of decimal places                                |
| Round down (floor)            | Rounds numbers down to the nearest integer                                              |
| Round up (ceiling)            | Rounds numbers up to the nearest integer                                                |
