document.addEventListener("DOMContentLoaded", function () {
  function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.getAll(name);
  }

  document.querySelectorAll(".tom-select-filter").forEach((el) => {
    const url = el.dataset.url;
    const param = el.dataset.param;

    const select = new TomSelect(el, {
      valueField: "value",
      labelField: "label",
      searchField: "label",
      plugins: ['remove_button'],
      load: function (query, callback) {
        const fullUrl = `${url}&q=${encodeURIComponent(query)}`;
        console.log({fullUrl})
        fetch(fullUrl)
          .then((res) => res.json())
          .then((json) => callback(json))
          .catch(() => callback());
      },
      onChange: function () {
        const values = el.tomselect.getValue();
        const searchParams = new URLSearchParams(window.location.search);
        if (values.length) {
          searchParams.set(param, values.join(","));
        } else {
          searchParams.delete(param);
        }
        window.location.search = searchParams.toString();
      },
      onFocus: function() {
        if (!this.input.value && this.items.length === 0) {
          this.load('');
        }
      }
    });

    const initialValues = getUrlParameter(param);  // adjust param name
    if (initialValues.length > 0) {
      const url = select.input.getAttribute('data-url');
      fetch(`${url}&q=${initialValues.join(',')}`) // TODO
        .then(res => res.json())
        .then(data => {
          // Add the initial options so Tom Select can render labels
          data.forEach(item => {
            // add option if not already present
            if (!select.options.hasOwnProperty(item.value)) {
              select.addOption(item);
            }
          });
          // set selected values
          select.setValue(initialValues);
        });
    }
  });
});
