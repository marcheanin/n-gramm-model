import os
import pickle
import argparse
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", dest="model_path", required=True)
    parser.add_argument("--prefix", dest="prefix", required=False)
    parser.add_argument("--length", dest="length", required=True)

    args = parser.parse_args()

    model_path = args.model_path
    length = int(args.length)

    if not os.path.isfile(model_path):
        raise OSError("Model not found")
    else:
        print("Model found!")
        with open(model_path, "rb") as f:
            data = pickle.load(f)

    print("Start genering...")
    # выбираем начало текста
    if args.prefix is not None:
        prefix = args.prefix.split()
        ans = prefix
    else:
        ans = [random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys()))))]

    i = len(ans) - 1

    # если текст ответа состоит из 1 символа, можем сгенерировать только по одному
    while len(ans) < 2:
        if ans[i] in data:
            # если префикс есть в тексте, генерируем новое слово из модели
            ans.append(random.choice(data[ans[i]]))
        else:
            # если префикса нет, берем рандомное слово из встречающихся в модели
            ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))
        i += 1

    # если текст ответа состоит из 2 символов, аналогично генерируем по двум
    while len(ans) < 3:
        bigram = (ans[i - 1], ans[i])
        if bigram in data:
            ans.append(random.choice(data[bigram]))
        elif ans[i] in data:
            ans.append(random.choice(data[ans[i]]))
        else:
            ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))
        i += 1

    # если в тексте больше 2 символов, генерируем по трем
    while i < length - 1:
        trigram = (ans[i - 2], ans[i - 1], ans[i])
        bigram = (ans[i - 1], ans[i])

        if trigram in data:
            ans.append(random.choice(data[trigram]))
        elif bigram in data:
            ans.append(random.choice(data[bigram]))
        elif ans[i] in data:
            ans.append(random.choice(data[ans[i]]))
        else:
            ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))

        i += 1

    print(' '.join(ans))


if __name__ == '__main__':
    main()
