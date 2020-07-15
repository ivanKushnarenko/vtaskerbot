import pickle


TASK_LIST = []


def insert_task(text: str):
    TASK_LIST.append(text)
    with open('list', 'wb') as f:
        pickle.dump(TASK_LIST, f)
