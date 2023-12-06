<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    v-bind:id="svgId"
    viewBox="-182 -182 364 364"
    width="380"
    height="380"
    style="font-size: 14px; font-family: Arial,Helvetica Neue,Helvetica,sans-serif;"
  >
    <g class="backlights">

      <path class="openness-to-change" d="M 0,0 L 0,-180 A 180 180 0 0 1 164.84 -72.31 z" fill="white"></path>
      <path class="self-enhancement" d="M 0,0 L 164.84,-72.31 A 180 180 0 0 1 110.56 142.05 z" fill="white"></path>
      <path class="conservation" d="M 0,0 L 110.56,142.05 A 180 180 0 0 1 -174.49 44.19 z" fill="white"></path>
      <path class="self-transcendence" d="M 0,0 L -174.49,44.19 A 180 180 0 0 1 0,-180 z" fill="white"></path>

      <path class="self-direction-thought openness-to-change personal-focus growth" d="M 0,0 L 0,-160 A 160 160 0 0 1 51.95 -151.33 z" fill="white"></path>
      <path class="self-direction-action openness-to-change personal-focus growth" d="M 0,0 L 51.95,-151.33 A 160 160 0 0 1 98.27 -126.26 z" fill="white"></path>
      <path class="stimulation openness-to-change personal-focus growth" d="M 0,0 L 98.27,-126.26 A 160 160 0 0 1 133.95 -87.51 z" fill="white"></path>
      <path class="hedonism openness-to-change self-enhancement personal-focus growth" d="M 0,0 L 133.95,-87.51 A 160 160 0 0 1 155.10 -39.28 z" fill="white"></path>
      <path class="achievement self-enhancement personal-focus growth self-protection" d="M 0,0 L 155.10,-39.28 A 160 160 0 0 1 159.45 13.21 z" fill="white"></path>
      <path class="power-dominance self-enhancement personal-focus self-protection" d="M 0,0 L 159.45,13.21 A 160 160 0 0 1 146.52 64.27 z" fill="white" ></path>
      <path class="power-resources self-enhancement personal-focus self-protection" d="M 0,0 L 146.42,64.27 A 160 160 0 0 1 117.72 108.37" fill="white" ></path>
      <path class="face self-enhancement conservation personal-focus self-protection" d="M 0,0 L 117.72,108.37 A 160 160 0 0 1 76.15 140.72 z" fill="white" ></path>
      <path class="security-personal conservation personal-focus self-protection" d="M 0,0 L 76.15,140.72 A 160 160 0 0 1 26.33 157.82 z" fill="white"></path>
      <path class="security-societal conservation social-focus self-protection" d="M 0,0 L 26.33,157.82 A 160 160 0 0 1 -26.33 157.82 z" fill="white"></path>
      <path class="tradition conservation social-focus self-protection" d="M 0,0 L -76.15,140.72 A 160 160 0 0 0 -26.33 157.82 z" fill="white"></path>
      <path class="conformity-rules conservation social-focus self-protection" d="M 0,0 L -117.72,108.37 A 160 160 0 0 0 -76.15 140.72 z" fill="white"></path>
      <path class="conformity-interpersonal conservation social-focus self-protection" d="M 0,0 L -146.52,64.27 A 160 160 0 0 0 -117.72 108.37 z" fill="white"></path>
      <path class="humility conservation self-transcendence social-focus self-protection growth" d="M 0,0 L -159.45,13.21 A 160 160 0 0 0 -146.52 64.27 z" fill="white"></path>
      <path class="benevolence-caring self-transcendence social-focus growth" d="M 0,0 L -155.10,-39.28 A 160 160 0 0 0 -159.45 13.21 z" fill="white" ></path>
      <path class="benevolence-dependability self-transcendence social-focus growth" d="M 0,0 L -133.95,-87.51 A 160 160 0 0 0 -155.10 -39.28 z" fill="white"></path>
      <path class="universalism-concern self-transcendence social-focus growth" d="M 0,0 L -98.27,-126.26 A 160 160 0 0 0 -133.95 -87.51 z" fill="white"></path>
      <path class="universalism-nature self-transcendence social-focus growth" d="M 0,0 L -51.95,-151.33 A 160 160 0 0 0 -98.27 -126.26 z" fill="white"></path>
      <path class="universalism-tolerance self-transcendence social-focus growth" d="M 0,0 L 0,-160 A 160 160 0 0 0 -51.95 -151.33 z" fill="white"></path>
    </g>

    <g class="labels">
      <path id="pathSelfDirection" d="M 0,-146 A 146 146 0 0 1 0 146" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathSelfDirection" startOffset="48.28">Self-direction:</textPath></text>
      <path id="pathPower" d="M 114.77,105.66 A 156 156 0 0 0 156 0" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathPower" startOffset="51.59">Power:</textPath></text>
      <path id="pathSecurity" d="M -25.68,153.87 A 156 156 0 0 0 156 0" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathSecurity" startOffset="51.59">Security:</textPath></text>
      <path id="pathConformity" d="M -142.86,62.66 A 156 156 0 0 0 156 0" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathConformity" startOffset="51.59">Conformity:</textPath></text>
      <path id="pathBenevolence" d="M -145.50,12.06 A 146 146 0 0 1 0 -146" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathBenevolence" startOffset="48.28">Benevolence:</textPath></text>
      <path id="pathUniversalism" d="M -122.23,-79.85 A 146 146 0 0 1 0 -146" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathUniversalism" startOffset="72.42">Universalism:</textPath></text>
      <text transform="translate(134 5) rotate(-80.53 -134 -5)" text-anchor="end">thought</text>
      <text transform="translate(134 5) rotate(-61.58 -134 -5)" text-anchor="end">action</text>
      <text transform="translate(155 5) rotate(-42.63 -155 -5)" text-anchor="end">Stimulation</text>
      <text transform="translate(155 5) rotate(-23.68 -155 -5)" text-anchor="end">Hedonism</text>
      <text transform="translate(155 5) rotate(-4.74 -155 -5)" text-anchor="end">Achievement</text>
      <text transform="translate(134 5) rotate(14.21 -134 -5)" text-anchor="end">dominance</text>
      <text transform="translate(134 5) rotate(33.16 -134 -5)" text-anchor="end">resources</text>
      <text transform="translate(155 5) rotate(52.11 -155 -5)" text-anchor="end">Face</text>
      <text transform="translate(134 5) rotate(71.05 -134 -5)" text-anchor="end">personal</text>
      <text transform="translate(-134 5) rotate(-90 134 -5)" text-anchor="start">societal</text>
      <text transform="translate(-155 5) rotate(-71.05 155 -5)" text-anchor="start">Tradition</text>
      <text transform="translate(-134 5) rotate(-52.11 134 -5)" text-anchor="start">rules</text>
      <text transform="translate(-134 5) rotate(-33.16 134 -5)" text-anchor="start">interpersonal</text>
      <text transform="translate(-155 5) rotate(-14.21 155 -5)" text-anchor="start">Humility</text>
      <text transform="translate(-134 5) rotate(4.74 134 -5)" text-anchor="start">caring</text>
      <text transform="translate(-134 5) rotate(23.68 134 -5)" text-anchor="start">dependability</text>
      <text transform="translate(-134 5) rotate(42.63 134 -5)" text-anchor="start">concern</text>
      <text transform="translate(-134 5) rotate(61.58 134 -5)" text-anchor="start">nature</text>
      <text transform="translate(-134 5) rotate(80.53 134 -5)" text-anchor="start">tolerance</text>

      <path id="pathOpennessToChange" d="M 0,-166 A 166 166 0 0 1 166 0" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathOpennessToChange" startOffset="96.06">Openness to change</textPath></text>
      <path id="pathSelfEnhancement" d="M 108.10,138.89 A 176 176 0 0 0 156.82 -79.90" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathSelfEnhancement" startOffset="116.40">Self-enhancement</textPath></text>
      <path id="pathConservation" d="M -170.61,43.21 A 176 176 0 0 0 124.45 124.45" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathConservation" startOffset="174.61">Conservation</textPath></text>
      <path id="pathSelfTranscendence" d="M -160.92,40.75 A 166 166 0 0 1 0 -166" fill="white" fill-opacity="0"></path>
      <text text-anchor="middle"><textPath href="#pathSelfTranscendence" startOffset="150.95">Self-transcendence</textPath></text>
    </g>

    <g class="interaction">
      <path class="self-direction-thought openness-to-change personal-focus growth" d="M 0,0 L 0,-160 A 160 160 0 0 1 51.95 -151.33 z" fill="white" fill-opacity="0"></path>
      <path class="self-direction-action openness-to-change personal-focus growth" d="M 0,0 L 51.95,-151.33 A 160 160 0 0 1 98.27 -126.26 z" fill="white" fill-opacity="0"></path>
      <path class="stimulation openness-to-change personal-focus growth" d="M 0,0 L 98.27,-126.26 A 160 160 0 0 1 133.95 -87.51 z" fill="white" fill-opacity="0"></path>
      <path class="hedonism openness-to-change self-enhancement personal-focus growth" d="M 0,0 L 133.95,-87.51 A 160 160 0 0 1 155.10 -39.28 z" fill="white" fill-opacity="0"></path>
      <path class="achievement self-enhancement personal-focus growth self-protection" d="M 0,0 L 155.10,-39.28 A 160 160 0 0 1 159.45 13.21 z" fill="white" fill-opacity="0"></path>
      <path class="power-dominance self-enhancement personal-focus self-protection" d="M 0,0 L 159.45,13.21 A 160 160 0 0 1 146.52 64.27 z" fill="white" fill-opacity="0"></path>
      <path class="power-resources self-enhancement personal-focus self-protection" d="M 0,0 L 146.42,64.27 A 160 160 0 0 1 117.72 108.37" fill="white" fill-opacity="0"></path>
      <path class="face self-enhancement conservation personal-focus self-protection" d="M 0,0 L 117.72,108.37 A 160 160 0 0 1 76.15 140.72 z" fill="white" fill-opacity="0"></path>
      <path class="security-personal conservation personal-focus self-protection" d="M 0,0 L 76.15,140.72 A 160 160 0 0 1 26.33 157.82 z" fill="white" fill-opacity="0"></path>
      <path class="security-societal conservation social-focus self-protection" d="M 0,0 L 26.33,157.82 A 160 160 0 0 1 -26.33 157.82 z" fill="white" fill-opacity="0"></path>
      <path class="tradition conservation social-focus self-protection" d="M 0,0 L -76.15,140.72 A 160 160 0 0 0 -26.33 157.82 z" fill="white" fill-opacity="0"></path>
      <path class="conformity-rules conservation social-focus self-protection" d="M 0,0 L -117.72,108.37 A 160 160 0 0 0 -76.15 140.72 z" fill="white" fill-opacity="0"></path>
      <path class="conformity-interpersonal conservation social-focus self-protection" d="M 0,0 L -146.52,64.27 A 160 160 0 0 0 -117.72 108.37 z" fill="white" fill-opacity="0"></path>
      <path class="humility conservation self-transcendence social-focus self-protection growth" d="M 0,0 L -159.45,13.21 A 160 160 0 0 0 -146.52 64.27 z" fill="white" fill-opacity="0"></path>
      <path class="benevolence-caring self-transcendence social-focus growth" d="M 0,0 L -155.10,-39.28 A 160 160 0 0 0 -159.45 13.21 z" fill="white" fill-opacity="0"></path>
      <path class="benevolence-dependability self-transcendence social-focus growth" d="M 0,0 L -133.95,-87.51 A 160 160 0 0 0 -155.10 -39.28 z" fill="white" fill-opacity="0"></path>
      <path class="universalism-concern self-transcendence social-focus growth" d="M 0,0 L -98.27,-126.26 A 160 160 0 0 0 -133.95 -87.51 z" fill="white" fill-opacity="0"></path>
      <path class="universalism-nature self-transcendence social-focus growth" d="M 0,0 L -51.95,-151.33 A 160 160 0 0 0 -98.27 -126.26 z" fill="white" fill-opacity="0"></path>
      <path class="universalism-tolerance self-transcendence social-focus growth" d="M 0,0 L 0,-160 A 160 160 0 0 0 -51.95 -151.33 z" fill="white" fill-opacity="0"></path>
    </g>

    <g class="outline">
      <circle cx="0" cy="0" r="160" fill="none" stroke="black"></circle>
      <line x1="0" y1="0" x2="0" y2="-160" stroke="black"></line>
      <line x1="0" y1="0" x2="46.11" y2="-134.31" stroke="black"></line>
      <line x1="0" y1="0" x2="98.27" y2="-126.26" stroke="black"></line>
      <line x1="0" y1="0" x2="133.95" y2="-87.51" stroke="black"></line>
      <line x1="0" y1="0" x2="155.10" y2="-39.28" stroke="black"></line>
      <line x1="0" y1="0" x2="159.45" y2="13.21" stroke="black"></line>
      <line x1="0" y1="0" x2="130.04" y2="57.04" stroke="black"></line>
      <line x1="0" y1="0" x2="117.72" y2="108.37" stroke="black"></line>
      <line x1="0" y1="0" x2="76.15" y2="140.72" stroke="black"></line>
      <line x1="0" y1="0" x2="23.37" y2="140.06" stroke="black"></line>
      <line x1="0" y1="0" x2="-26.34" y2="157.82" stroke="black"></line>
      <line x1="0" y1="0" x2="-76.15" y2="140.72" stroke="black"></line>
      <line x1="0" y1="0" x2="-104.47" y2="96.17" stroke="black"></line>
      <line x1="0" y1="0" x2="-146.52" y2="64.27" stroke="black"></line>
      <line x1="0" y1="0" x2="-159.45" y2="13.21" stroke="black"></line>
      <line x1="0" y1="0" x2="-137.65" y2="-34.86" stroke="black"></line>
      <line x1="0" y1="0" x2="-133.94" y2="-87.51" stroke="black"></line>
      <line x1="0" y1="0" x2="-87.22" y2="-112.06" stroke="black"></line>
      <line x1="0" y1="0" x2="-46.11" y2="-134.31" stroke="black"></line>

      <circle cx="0" cy="0" r="180" fill="none" stroke="black"></circle>
      <line x1="0" y1="-160" x2="0" y2="-180" stroke="black"></line>
      <line x1="146.52" y1="-64.27" x2="164.84" y2="-72.30" stroke="black"></line>
      <line x1="98.27" y1="126.26" x2="110.56" y2="142.05" stroke="black"></line>
      <line x1="-155.10" y1="39.28" x2="-174.49" y2="44.19" stroke="black"></line>
    </g>
  </svg>
</template>

<!--<style scoped>-->
<!--  svg#metric-continuum > g.interaction > path {-->
<!--    cursor: pointer;-->
<!--  }-->
<!--</style>-->

<script lang="ts">

  const values: any = {
    'self-direction-thought': [1,0,-160,51.95,-151.33],
    'self-direction-action': [1,51.95,-151.33,98.27,-126.26],
    'stimulation': [1,98.27,-126.26,133.95,-87.51],
    'hedonism': [1,133.95,-87.51,155.10,-39.28],
    'achievement': [1,155.10,-39.28,159.45,13.21],
    'power-dominance': [1,159.45,13.21,146.52,64.27],
    'power-resources': [1,146.42,64.27,117.72,108.37],
    'face': [1,117.72,108.37,76.15,140.72],
    'security-personal': [1,76.15,140.72,26.33,157.82],
    'security-societal': [1,26.33,157.82,-26.33,157.82],
    'tradition': [0,-76.15,140.72,-26.33,157.82],
    'conformity-rules': [0,-117.72,108.37,-76.15,140.72],
    'conformity-interpersonal': [0,-146.52,64.27,-117.72,108.37],
    'humility': [0,-159.45,13.21,-146.52,64.27],
    'benevolence-caring': [0,-155.10,-39.28,-159.45,13.21],
    'benevolence-dependability': [0,-133.95,-87.51,-155.10,-39.28],
    'universalism-concern': [0,-98.27,-126.26,-133.95,-87.51],
    'universalism-nature': [0,-51.95,-151.33,-98.27,-126.26],
    'universalism-tolerance': [0,0,-160,-51.95,-151.33]
  }

  export default {
    name: "metric-continuum",
    props: ["values", "id", "backgroundColor"],
    data() {
      return {
        svgValues: this.$props.values,
        svgId: this.$props.id
      }
    },
    mounted: function () {
      (this.svgValues as {name: string, value: number}[]).forEach(entry => {
        this.select(entry.name, entry.value)
      })
    },
    methods: {
      deselectAll () {
        console.debug('Now')
        document.querySelectorAll('svg#metric-continuum > g.backlights > path').forEach(
          path => path.setAttribute('fill', 'white')
        )
      },
      select (class_name: string, percentage: number) {
        percentage = Math.min(1.0, Math.max(0.0, percentage))
        let value = values[class_name]

        let coord1 = (value[1] * percentage) + "," + (value[2] * percentage)
        let coord2 = (value[3] * percentage) + " " + (value[4] * percentage)

        document.querySelectorAll('svg#' + this.svgId +' > g.backlights > path.' + class_name).forEach(
          path => {
            path.setAttribute(
              'd',
              "M 0,0 L " + coord1 + " A 160 160 0 0 " + value[0] + " " + coord2 + " z"
            )
            path.setAttribute('fill', this.$props.backgroundColor)
            // add hover tooltip
          }
        )
      },
    },
    setup (props) {
      (props.values as {name: string, value: number}[]).forEach(entry => {
        let class_name = entry.name
        let percentage = entry.value

        percentage = Math.min(1.0, Math.max(0.0, percentage))
        let value = values[class_name]

        let coord1 = (value[1] * percentage) + "," + (value[2] * percentage)
        let coord2 = (value[3] * percentage) + " " + (value[4] * percentage)

        document.querySelectorAll('svg#' + props.id +' > g.backlights > path.' + class_name).forEach(
          path => {
            path.setAttribute(
              'd',
              "M 0,0 L " + coord1 + " A 160 160 0 0 " + value[0] + " " + coord2 + " z"
            )
            path.setAttribute('fill', props.backgroundColor)
            // add hover tooltip
          }
        )
      })
    }
  }
</script>
