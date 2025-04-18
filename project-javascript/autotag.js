var a = 3
var b = 5
var name = "nithin"
a *=b

console.log(name.length)
console.log("2nd letter of the name is "+  name[name.length -1])




var list = [["nithin", "babu"], [11,23]]
console.log(list[0][1], list[1][0])

list.push(["sasi",65])
console.log(list)

list.pop()
console.log(list)

list.shift()
console.log(list)

list.unshift(["happy", 221])
console.log(list)

function sasi (age, location, gender) {
    return "sasi age is " + age + " and he is from " + location + " and is a " + gender
}
console.log(sasi(26,"thirumala","male"))

console.info(typeof(name))

function tureorfalse(isittrue) {
    if (isittrue){
        return "it is true"
    }
    return "it is false"
}

console.log(tureorfalse(false))


if (a<=50 && a>=25) {
  console.log("yes value is between this")   
} else {
    console.log("No value is not in this ranage")
}


var dic = {
    "name" : "nithin",
    "age" : 32,
    "hobbies": ["cricket", "football"]
}
var name = dic["name"]
var age = dic["age"]
console.log("MY name is "+ name + " and i am "+ age +" years old. and my hobbies are " + dic.hobbies[1])
dic.location = ["america","India"]
delete dic.age
console.log(dic)



function checkpro(checkobj) {
    if (dic.hasOwnProperty(checkobj)) {
        return dic[checkobj]
    } else {
        return "Not found"
    }
}

console.log(checkpro("name"))