import { bindEventListeners } from './form.js';
import { loadResults } from './storage.js';

window.onload = () => {
    loadResults();
    bindEventListeners();
}