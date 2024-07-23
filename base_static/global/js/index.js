const buttonCloseMenu = document.querySelector('.button-close-menu');
const buttonShowMenu = document.querySelector('.button-show-menu');
const menuContainer = document.querySelector('.menu-container');

const buttonShowMenuVisibleClass = 'button-show-menu-visible';
const menuHiddenClass = 'menu-hidden';

const closeMenu = () => {
  buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
  menuContainer.classList.add(menuHiddenClass);
};

const showMenu = () => {
  buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
  menuContainer.classList.remove(menuHiddenClass);
};

if (buttonCloseMenu) {
  buttonCloseMenu.removeEventListener('click', closeMenu);
  buttonCloseMenu.addEventListener('click', closeMenu);
}

if (buttonShowMenu) {
  buttonCloseMenu.removeEventListener('click', showMenu);
  buttonShowMenu.addEventListener('click', showMenu);
}


// Logout form
const logout = document.querySelector('form-logout')

logout.addEventListener('submit', function(e){
    e.preventDefault();

    logout.submit();
})


// Delete recipe
forms = document.querySelectorAll('.form-delete')

for(const form of forms) {
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const confirmed = confirm('Você realmente deseja deletar?');

        if(confirmed) {
            form.submit();
        }
    })

}