
filename = ('a.csv')
f = open (filename, 'a')


received_data = "2018-10-24 17:24:09.410926,.293,\nSenserZ:9.875,Y:5.6875,\nSenserZ:-15.0625\n"
saved_data = [' ', 'S', 'e', 'n', 's', 'e', 'r', 'Z', ':', '-', '1', '5', '.', '0', '6', '2', '5']
#tail_data ="830722656250001,0.3687070556640625,9.916783276367189"
'''received_data= "x:-0.081402856x:-0.0742202x:-0.08858546142578126,0.3x:-0.0622492431640625,0.3998316772460938,9.979032519531252x:-0.07182604980468752,0.3687070556640625,9.897629663085938x:-0.05027823486328126,0.4189852905273438,9.856928234863283x:-0.05506663818359376,0.3950432739257813,9.94790789794922x:-0.07900865478515627,0.3782838623046875,9.911994873046876x:-0.1364694946289063,0.373495458984375,9.90960067138672x:-0.05985504150390626,0.3519476440429688,9.921571679687501x:-0.08379705810546877,0.421379492187564746094x:-0.06943184814453125,0.3519476440429688,9.888052856445313x:-0.07661445312500001,0.3591302490234376,9.897629663085938"
'''


'''
for d in data:
    s.append(d)
    if(d=='\n'):
        break
    i=i+1
print(''.join(s))


'''
tail_data = ''.join(saved_data)
print("tail_data:"+tail_data)
print("received_data:"+ received_data)
received_data = tail_data + received_data
print("received_data:"+ received_data)

if(received_data[-1]=='\n'):
    print("改行だけだよ")
    received_data.split('\n')
    print(received_data)
#    log.write(received_data)
    f.write(received_data)
    #saved_dataを初期化
    saved_data=[]
else:
    print("改行で終わってないよ")
    spritdata = received_data.split('\n')
    i=0
    print(spritdata)
    #最後-1の要素を取得し
    while(i < len(spritdata)-1):

        print(spritdata[i])
#        log.write(spritdata[i])
        f.write(spritdata[i]+'\n')

        i=i+1
    string=spritdata[i]
    #分解
    for c in string:
        saved_data.append(c)
print(saved_data)
    #c.send(b'X:'+ x + b','+ b'Y:'+ y +b','+ b'Z:'+ z+b'\\n')
