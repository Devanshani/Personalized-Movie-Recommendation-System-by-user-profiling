import requests
import time
import random



# token="EAAdAP9BYA2MBADp2ZC0IPT5sv6ONfjyj5aGNNjL7vZAtwqCMrD0djDyLqqb8rh3NvPjhjeZCMliHHmWoPDC0OoIHmrelselLQJt29c6oioeZBH165H4ZCpG1OnZCJcXTLIkeMJYn8pEBbixiZBZABJFDFZANAItz9sWuNZAQv456dWsOMvjCWVGKsfgIUnC6ZBZBfJa0OduDmV0xgnTiZC6bLSpLcVrheYxabSkIZD"
# token="EAAdAP9BYA2MBADp2ZC0IPT5sv6ONfjyj5aGNNjL7vZAtwqCMrD0djDyLqqb8rh3NvPjhjeZCMliHHmWoPDC0OoIHmrelselLQJt29c6oioeZBH165H4ZCpG1OnZCJcXTLIkeMJYn8pEBbixiZBZABJFDFZANAItz9sWuNZAQv456dWsOMvjCWVGKsfgIUnC6ZBZBfJa0OduDmV0xgnTiZC6bLSpLcVrheYxabSkIZD"
# token="EAAdAP9BYA2MBAJcZCTh7jpsZBACDBUw66yhjXDfwK9qp6uU2m9ZC2qU5HAqjXRNVtbFCuZAieZBEyzHjlf1FrY1Udbrc1nlzNFvCxFbX33b2lBJOidewdZAkFeRoSOBNBrYG7bXdPOZAGCZCO7svjwQcLlkRIwLl4KDXoc5GRTFjLMxEALTp7uwZBiPSaliwrBluiZAeIlbtuzpb7Yj8GYB1iZC"
token="EAAdAP9BYA2MBAD3wSlAHvqLKgerQQPbgtrzaUQHl6XaMMmjsyJQyGRRB6u5sn9svnm39nxutWN2TCBUZC3FVZAqfDZBmNcabzjc0c4qU13v8JQYrvnndG4ZB20jUAZCUgZB38W2f3HbM4p6LbfhdsRZBsKCPCNZBuLhI3tgB81hReC5iO098M0Jxtv3AZCGsEliyh2bHLk2UimqauKMjU26ZBEyHOWShoaAKkZD"
def req_facebook(req):
    r=requests.get("https://graph.facebook.com/v2.10/"+req,{'access_token':token})
    return r
if __name__ == "__main__":
    req="224715188333734?fields=feed.limit(100),posts{message},likes"
    # req="1450895401697551?fields=feed.limit(400){full_picture,place,from,comments{message},message,likes.limit(0).summary(true)}"
    results=req_facebook(req).json()
    print(results)
    results=results['posts']
    data=[]
    # data.extend(result['data'])
    i=0
    data=[]
    print(results['data'])
    # while True:
    #     time.sleep(random.randint(2,5))
    #     data.extend(results['data'])
    #     r=requests.get(results['paging']['next'])
    #     results=r.json()
    #     i=+1
    # print(result['paging']['next'])
    #
    # rm=result['paging']['next']
    # r=requests.get(rm).json()
    # print("ggggg",r)
    # print(r['paging']['next'])

