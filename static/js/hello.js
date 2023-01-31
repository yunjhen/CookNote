
console.log("hello world~~~")

const userForm  = [...document.getElementsByClassName('user-form')]

const btn = document.getElementById('submit-button')
const userName = document.getElementById('user-name')

btn.addEventListener('click', ()=>{
    console.log('get', userName.value)
})
userName.addEventListener('keyup', ()=>{
    console.log('input', userName.value)
})
