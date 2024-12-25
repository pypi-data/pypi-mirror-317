from langchain_community.llms.tongyi import Tongyi

if __name__ == '__main__':
    tongyi = Tongyi(model_name='qwen2-1.5b-instruct',
                    dashscope_api_key='sk-839744c21b1f445d855a1137e7cc1225')
    print(tongyi.invoke('你是谁'))
