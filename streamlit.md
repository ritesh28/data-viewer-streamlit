```bash
streamlit run your_script.py [-- script args] # When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself.
```

## Caching

- `st.cache_data` is the recommended way to cache computations that return data. Use st.cache_data when you use a function that returns a serializable data object (e.g. str, int, float, DataFrame, dict, list). It creates a new copy of the data at each function call, making it safe against mutations and race conditions.
- `st.cache_resource` is the recommended way to cache global resources like ML models or database connections. Use st.cache_resource when your function returns unserializable objects that you don’t want to load multiple times. It returns the cached object itself, which is shared across all reruns and sessions without copying or duplication. If you mutate an object that is cached using st.cache_resource, that mutation will exist across all reruns and sessions.

```py
@st.cache_data
def long_running_function(param1, param2):
    return …
```

## Session State

```py
st.session_state.counter = 0
```

## Pages

Page
navigation

```py
import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()
```

## Display and style data

write
dataframe
table
line_chart
map

## widgets

button
slider
checkbox
selectbox

## Layout

sidebar
columns
expander

## Real time

progress

## Todo: youtube tech with tim

- st.write & magic
  - is called magic since it can write based on the type of variable being written
- data flow
- text element
  - st.title()
  - st.header() & st.subheader()
  - st.markdown()
  - st.code()
  - st.warning()
- images
  - put image inside `static` folder
  - `st.image(os.path.join(os.getcwd(), 'static', 'bg.jpg'))`
- data element
  - st.dataframe()
  - st.data_editor()
  - st.table()
  - st.metric()
  - st.json()
- chart element
  - st.area_chart()
  - st.bar_chart()
  - st.line_chart()
  - st.scatter_chart()
  - st.map()
  - st.pyplot()
- form element
  - key attribute
  - st.form() - rerun only when submit button is clicked. st.form_submit_button is mandatory
  - st.form_submit_button()
  - st.text_input()
  - st.text_area()
  - st.date_input()
  - st.time_input()
  - st.radio()
  - st.checkbox()
  - st.selectbox()
  - st.select_slider()
- session state
- callback
- layout
- advanced widget concept
- caching
- st.rerun
- fragment
- multi-page
- advanced page
