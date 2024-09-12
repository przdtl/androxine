

export function SignIn() {
    fetch('https://jsonplaceholder.typicode.com/photos')
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log(data);
            setPhotos(data);
        });
}

export function SignUp() {

}

export function SignOut() {

}