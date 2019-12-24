function getModal(e) {
        const post = e.target.parentElement.parentElement.cloneNode(true);
        const modalBackground = document.createElement('div');

        modalBackground.classList.add('modal__container');
        modalBackground.addEventListener('click', (e) => e.target==modalBackground&&e.target.remove())
        post.classList.add('modal');
        
        modalBackground.appendChild(post);
        document.body.appendChild(modalBackground);
}