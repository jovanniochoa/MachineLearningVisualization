document.addEventListener('DOMContentLoaded', function() {
  var tiles = document.querySelectorAll('.tile');

  for (var i = 0; i < tiles.length; i++) {
    tiles[i].addEventListener('click', function() {
      this.classList.toggle('active');
    });
  }
});

const wrapper = document.getElementById("tiles");
let columns = 0;
let rows = 0;
let toggled = false;

const toggle = () => {
  toggled = !toggled;

  document.body.classList.toggle("toggled");
}

const handleOnClick = index => {
  toggle();

  anime({
    targets: [".tile", "#title", ".fancy", "#icon"],
    opacity: toggled ? 0 : 1,
    delay: anime.stagger(50, {
      grid: [columns, rows],
      from: index
    }),
    duration: 500 // Set the duration to 500 milliseconds
  });
  

  // Toggle the visibility of the "Get Started" button
  const button = document.querySelector('.button');
  button.style.display = toggled ? 'none' : 'block';
}


const createTile = index => {
  const tile = document.createElement("div");

  tile.classList.add("tile");

  tile.style.opacity = toggled ? 0 : 1;

  tile.onclick = e => handleOnClick(index);

  return tile;
}

const createGrid = () => {
  const size = document.body.clientWidth > 800 ? 100 : 50;

  columns = 15;
  rows = 15;

  wrapper.style.setProperty("--columns", columns);
  wrapper.style.setProperty("--rows", rows);

  for (let i = 0; i < columns * rows; i++) {
    wrapper.appendChild(createTile(i));
  }
}

createGrid();

window.onresize = () => {
  wrapper.innerHTML = "";
  createGrid();
};
