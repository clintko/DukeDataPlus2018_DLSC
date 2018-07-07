import pandas as pd


def attach_label(label, raw):
    data_label = pd.read_csv(label, sep="\t", header="infer", index_col=0)
    data_label = data_label.values
    data_raw = pd.read_csv(raw, sep=",", header="infer", index_col=0)
    data_label = data_label.reshape(len(data_label))
    print(data_label)
    data_raw.index = list(i.replace("\'", "").replace("(", "").replace(")", "") for i in data_label)
    data_raw.to_csv("./data/data_indexed_with_label_transposed.csv")


if __name__ == "__main__":
    attach_label("./data/data_label.tsv", "./data/data_with_label_transposed.csv")
