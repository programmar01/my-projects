const num1 = Math.ceil(Math.random() * 10)
const num2 = Math.ceil(Math.random() * 10)

const questionEl = document.getElementById("question");
const scoreEl = document.getElementById("score");
const formEl = document.getElementById("form");
const inputEl = document.getElementById("input")

questionEl.innerText = `What will be ${num1} multiplied by ${num2}?`


const correctAns = num1 * num2

let score = JSON.parse(localStorage.getItem("score"));
if(!score){
    score = 0;
}

scoreEl.innerText = `Score: ${score}`

formEl.addEventListener("submit", ()=>{
    const userAnswer = +inputEl.value
    if(correctAns === userAnswer){
        score++
        updateLocalStorage()
    }else{
        score--
        updateLocalStorage()
    }


})


function updateLocalStorage(){
    localStorage.setItem("score", JSON.stringify(score))

}

function updateLocalStorage(){
    localStorage.setItem("score", JSON.stringify(score))

}