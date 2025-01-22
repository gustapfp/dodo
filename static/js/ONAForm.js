const onaJsonForm = JSON.parse(document.getElementById('ona_json').textContent);
console.log(onaJsonForm)
const showFirstSection = ()=> {
    let firstSection = onaJsonForm['ONA_sections'][0]['section_title']
    firstSection = document.getElementById(firstSection)
    firstSection.classList.remove('hidden');
    firstSection.classList.add('visible');
}

const showFirstSubsection = ()=> {
    let firstSubSection = onaJsonForm['ONA_sections'][0]['form_subsections'][0]['subsection_title']
    firstSubSection = document.getElementById(firstSubSection)
    firstSubSection.classList.remove('hidden');
    firstSubSection.classList.add('visible');
}
showFirstSection()
showFirstSubsection()



const showNextElement = (sectionHTMLElement) => {
    const section = document.getElementById(sectionHTMLElement)
    if (section.classList.contains('hidden')) {

        section.classList.remove('hidden');
        section.classList.add('visible');
    } else {
  
        section.classList.remove('visible');
        section.classList.add('hidden');
    }    
}

