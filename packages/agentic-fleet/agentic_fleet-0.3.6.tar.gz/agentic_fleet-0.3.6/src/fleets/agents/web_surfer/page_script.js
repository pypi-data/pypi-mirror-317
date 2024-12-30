// Page script for browser automation
function getElementInfo(element) {
    const rect = element.getBoundingClientRect();
    const computedStyle = window.getComputedStyle(element);
    
    return {
        tag: element.tagName.toLowerCase(),
        text: element.textContent.trim(),
        attributes: Array.from(element.attributes).reduce((acc, attr) => {
            acc[attr.name] = attr.value;
            return acc;
        }, {}),
        xpath: getXPath(element),
        isVisible: isElementVisible(element),
        position: {
            x: rect.left + window.scrollX,
            y: rect.top + window.scrollY,
            width: rect.width,
            height: rect.height
        },
        style: {
            display: computedStyle.display,
            visibility: computedStyle.visibility,
            opacity: computedStyle.opacity,
            zIndex: computedStyle.zIndex
        }
    };
}

function getXPath(element) {
    if (!element) return '';
    if (element === document.body) return '/html/body';
    
    let path = '';
    let current = element;
    
    while (current && current !== document.body) {
        let index = 1;
        let sibling = current;
        
        while (sibling = sibling.previousElementSibling) {
            if (sibling.tagName === current.tagName) {
                index++;
            }
        }
        
        const tag = current.tagName.toLowerCase();
        path = `/${tag}[${index}]${path}`;
        current = current.parentElement;
    }
    
    return `/html/body${path}`;
}

function isElementVisible(element) {
    const style = window.getComputedStyle(element);
    
    return style.display !== 'none' &&
           style.visibility !== 'hidden' &&
           style.opacity !== '0' &&
           element.offsetWidth > 0 &&
           element.offsetHeight > 0;
}

function findElementsByText(text, caseSensitive = false) {
    const pattern = caseSensitive ? text : text.toLowerCase();
    const elements = [];
    
    function traverse(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const content = caseSensitive ? node.textContent : node.textContent.toLowerCase();
            if (content.includes(pattern)) {
                elements.push(node.parentElement);
            }
        } else {
            node.childNodes.forEach(traverse);
        }
    }
    
    traverse(document.body);
    return elements.map(getElementInfo);
}

function findElementsBySelector(selector) {
    try {
        const elements = Array.from(document.querySelectorAll(selector));
        return elements.map(getElementInfo);
    } catch (e) {
        console.error('Invalid selector:', e);
        return [];
    }
}

function getPageMetadata() {
    return {
        url: window.location.href,
        title: document.title,
        description: document.querySelector('meta[name="description"]')?.content || '',
        keywords: document.querySelector('meta[name="keywords"]')?.content || '',
        author: document.querySelector('meta[name="author"]')?.content || '',
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight,
            scrollX: window.scrollX,
            scrollY: window.scrollY
        }
    };
}

function extractLinks() {
    return Array.from(document.links).map(link => ({
        text: link.textContent.trim(),
        url: link.href,
        title: link.title || '',
        target: link.target || '',
        isExternal: link.hostname !== window.location.hostname
    }));
}

function extractImages() {
    return Array.from(document.images).map(img => ({
        src: img.src,
        alt: img.alt || '',
        title: img.title || '',
        width: img.width,
        height: img.height,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        isLoaded: img.complete && img.naturalHeight !== 0
    }));
}

function extractForms() {
    return Array.from(document.forms).map(form => ({
        id: form.id || '',
        name: form.name || '',
        method: form.method,
        action: form.action,
        elements: Array.from(form.elements).map(element => ({
            type: element.type || '',
            name: element.name || '',
            id: element.id || '',
            value: element.type === 'password' ? '' : element.value,
            isRequired: element.required,
            isDisabled: element.disabled
        }))
    }));
}

// Export functions for external use
window.pageTools = {
    getElementInfo,
    findElementsByText,
    findElementsBySelector,
    getPageMetadata,
    extractLinks,
    extractImages,
    extractForms
}; 