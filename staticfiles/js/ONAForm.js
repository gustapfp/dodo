const onaJsonForm = JSON.parse(document.getElementById('ona_json').textContent);

// const showFirstSection = ()=> {
//     let firstSection = onaJsonForm['ONA_sections'][0]['section_title']
//     firstSection = document.getElementById(firstSection)
//     firstSection.classList.remove('hidden');
//     firstSection.classList.add('visible');
// }

// const showFirstSubsection = ()=> {
//     let firstSubSection = onaJsonForm['ONA_sections'][0]['form_subsections'][0]['subsection_title']
//     firstSubSection = document.getElementById(firstSubSection)
//     firstSubSection.classList.remove('hidden');
//     firstSubSection.classList.add('visible');
// }



// const showNextSubsection = (sectionHTMLElement) => {
//     const subSection = document.getElementById(sectionHTMLElement)
//     if (subSection.classList.contains('hidden')) {
        
//         subSection.classList.remove('hidden');
//         subSection.classList.add('visible');
//     } else {
        
//         subSection.classList.remove('visible');
//         subSection.classList.add('hidden');
//     }    
// }

// showFirstSection()
// showFirstSubsection()
