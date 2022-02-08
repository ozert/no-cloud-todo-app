import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import yaml
def read_config(path:str) -> tuple:
    assert(isinstance(path,str) and (path.endswith(".yaml") or path.endswith(".yml")))#It must be string have ".yml" or ".yaml" extention.
    with open(path, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    content = [(entry["item"]["text"], entry["item"]["status"]) for entry in config["todo_items"]]
    return content
def update_config(config_content:dict, path:str) -> None:
    assert(isinstance(path,str) and (path.endswith(".yaml") or path.endswith(".yml")))#It must be string have ".yml" or ".yaml" extention.
    with open(path, 'w') as file:
        outputs = yaml.dump(config_content, file)
    return None
progress=0
st.title('TODO:')
st.text("This is the TODO tasks in my mindmap.")
my_bar = st.progress(0)
config_content = read_config(path='todo_config.yml')
todo_items = [item for item in config_content]
#Add new items
new_entry = st.text_input('Add New Item',"")
if new_entry != "":
    todo_items.append((new_entry,False))

todo_items.sort(key=lambda x: x[1])

with st.form("my_form"):
    checkboxes = [st.checkbox(todo_item, value=status) for todo_item,status in todo_items]
    submitted = st.form_submit_button("Submit")
    my_bar.progress([status for _, status in todo_items].count(True)*100//len(checkboxes))
    if submitted:
        progress = [True if chckbox else False for chckbox in checkboxes]
        todo_items = [(item[0],status) for item,status in zip(todo_items, progress)]
        total_percentage = progress.count(True)*100//len(checkboxes)
        if total_percentage ==100:
            st.success("Nothing left in here you need to complete :)")
        else:
            st.warning("There you go! :)")
        my_bar.progress(total_percentage)
        st.write("Completion percentage: ", total_percentage)
        updated_config = {"todo_items":[{"item":{"text": todo_item, "status": status}} for (todo_item, status) in todo_items]}
        update_config(config_content=updated_config, path='todo_config.yml')
