const hide = (element) => {
    element.style.display = 'none';
};
const show = (element) => {
    element.style.display = 'block';
};

const initTournamentEntry = (container) => {
    const memberSelect = container.getElementsByClassName('member-select').item(0);
    const form = container.getElementsByClassName('form').item(0);
    if (memberSelect) {
        hide(form);

        Array.from(memberSelect.getElementsByClassName('btn')).forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if (btn.dataset.name) {
                    document.getElementById('id_name').value = btn.dataset.name;
                    document.getElementById('id_club').value = 'Wallingford Castle Archers';
                    document.getElementById('id_date_of_birth').value = btn.dataset.dob;
                    document.getElementById('id_agb_number').value = btn.dataset.agb;
                }
                hide(memberSelect);
                show(form);
            });
        });
    }
};

export default initTournamentEntry;
