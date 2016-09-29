''' sample dream '''
from dreamer import Dream

if __name__ == "__main__":
    dream = Dream(dream_type='sex')
    for i in range(10):
        print dream.dream()
