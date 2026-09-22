import { bindEventListeners } from './form.js';
import { loadResults } from './resultTable.js';

window.onload = () => {
    loadResults();
    bindEventListeners();
}