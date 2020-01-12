from functools import reduce

def bitstring_to_bytes(bit_s):
    return int(bit_s, 2).to_bytes((len(bit_s) + 7) // 8, byteorder='big')

def bytes_to_bit_string(bytes):
    return bin(int(bytes.hex(), base = 16))[2:]

def gap_encoding(list_to_encode):
    result = copy(list_to_encode)

    for i in range(1, len(result)):
        result[i] = list_to_encode[i] - list_to_encode[i - 1]

    return result

def gap_decoding(list_to_decode):
    result = copy(list_to_decode)

    for i in range(1, len(result)):
        result[i] = list_to_encode[i] + result[i - 1]

    return result


def gamma_encoding(postings):
    return "".join([get_length(get_offset(gap))+get_offset(gap) for gap in get_gaps_list(postings)])

def gamma_decoding(gamma):
    num,length,offset,aux,res = 0,"","",0,[]
    while gamma!="":
        aux    = gamma.find("0")
        length = gamma[:aux]
        if length=="": res.append(1); gamma = gamma[1:]
        else:
            offset = "1"+gamma[aux+1:aux+1+unary_decodification(length)]
            res.append(int(offset,2))
            gamma  = gamma[aux+1+unary_decodification(length):]
    return res


def get_offset(gap): return bin(gap)[3:]
def get_length(offset): return unary_codification(len(offset))+"0"
def unary_codification(gap):  return "".join(["1" for _ in range(gap)])
def unary_decodification(gap): return reduce(lambda x,y : int(x)+int(y),list(gap))
def get_gaps_list(posting_lists): return [posting_lists[0]]+[posting_lists[i]-posting_lists[i-1] for i in range(1,len(posting_lists))]


if __name__ == '__main__':
    print(gamma_encoding([10,15,22,23,34,44,50,58]))
    print(type(gamma_encoding([10,15,22,23,34,44,50,58])))
    print(gamma_decoding(gamma_encoding([10,15,22,23,34,44,50,58])))
