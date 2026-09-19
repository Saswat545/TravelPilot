/* Lucide Icons — sourced via: better-icons get lucide:<name>
   All icons use consistent 24x24 viewBox, stroke="currentColor", strokeWidth="2" */

const iconPaths = {
  plane: 'M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8L4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1l3 2l2 3l1-1v-3l3-2l3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2',
  mapPin: { paths: ['M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0', { tag: 'circle', cx: 12, cy: 10, r: 3 }] },
  calendar: { paths: ['M8 2v3m8-3v3', { tag: 'rect', width: 18, height: 18, x: 3, y: 3, rx: 2 }, 'M3 9h18M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01'] },
  dollarSign: 'M12 2v20m5-17H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6',
  users: { paths: ['M18 21a8 8 0 0 0-16 0', { tag: 'circle', cx: 10, cy: 8, r: 5 }, 'M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3'] },
  zap: 'M15.914 4a1.5 1.5 0 0 0-2.474-1.561l-9 9A1.5 1.5 0 0 0 5.5 14h4.002a.5.5 0 0 1 .471.666L8.086 20a1.5 1.5 0 0 0 2.475 1.56l9-9A1.5 1.5 0 0 0 18.5 10h-3.997a.5.5 0 0 1-.472-.667z',
  alertTriangle: 'm21.73 18l-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3M12 9v4m0 4h.01',
  clock: { paths: [{ tag: 'circle', cx: 12, cy: 12, r: 10 }, 'M12 6v6l4 2'] },
  arrowRight: 'M5 12h14m-7-7l7 7l-7 7',
  send: 'M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11zm7.318-19.539l-10.94 10.939',
  messageCircle: 'M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092a10 10 0 1 0-4.777-4.719',
  trendingUp: { paths: ['M16 7h6v6', 'm22 7l-8.5 8.5l-5-5L2 17'] },
  barChart3: 'M3 3v18h18m-3-4V9m-5 8V5M8 17v-3',
  shieldCheck: { paths: ['M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z', 'm9 12l2 2l4-4'] },
  cpu: { paths: ['M12 20v2m0-20v2m5 16v2m0-20v2M2 12h2m-2 5h2M2 7h2m16 5h2m-2 5h2M20 7h2M7 20v2M7 2v2', { tag: 'rect', width: 16, height: 16, x: 4, y: 4, rx: 2 }, { tag: 'rect', width: 8, height: 8, x: 8, y: 8, rx: 1 }] },
  wrench: 'M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z',
  settings: { paths: ['M9.671 4.136a2.34 2.34 0 0 1 4.659 0a2.34 2.34 0 0 0 3.319 1.915a2.34 2.34 0 0 1 2.33 4.033a2.34 2.34 0 0 0 0 3.831a2.34 2.34 0 0 1-2.33 4.033a2.34 2.34 0 0 0-3.319 1.915a2.34 2.34 0 0 1-4.659 0a2.34 2.34 0 0 0-3.32-1.915a2.34 2.34 0 0 1-2.33-4.033a2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915', { tag: 'circle', cx: 12, cy: 12, r: 3 }] },
  landmark: 'M10 18v-7m1.119-8.795a2 2 0 0 1 1.762 0l7.84 3.846A.5.5 0 0 1 20.5 7h-17a.5.5 0 0 1-.22-.949zM14 18v-7m4 7v-7M3 22h18M6 18v-7',
  utensils: 'M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20m14-7V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2zm0 0v7',
  treePine: 'm17 14l3 3.3a1 1 0 0 1-.7 1.7H4.7a1 1 0 0 1-.7-1.7L7 14h-.3a1 1 0 0 1-.7-1.7L9 9h-.2A1 1 0 0 1 8 7.3L12 3l4 4.3a1 1 0 0 1-.8 1.7H15l3 3.3a1 1 0 0 1-.7 1.7zm-5 8v-3',
  shoppingBag: { paths: ['M16 10a4 4 0 0 1-8 0M3.103 6.034h17.794', 'M3.4 5.467a2 2 0 0 0-.4 1.2V20a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6.667a2 2 0 0 0-.4-1.2l-2-2.667A2 2 0 0 0 17 2H7a2 2 0 0 0-1.6.8z'] },
  ticket: 'M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Zm11-4v2m0 10v2m0-8v2',
  mountain: 'm8 3l4 8l5-5l5 15H2z',
  sparkles: { paths: ['M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594zM20 2v4m2-2h-4', { tag: 'circle', cx: 4, cy: 20, r: 2 }] },
}

function renderIcon(name, props = {}) {
  const d = iconPaths[name]
  if (!d) return null

  const children = []
  const items = typeof d === 'string' ? [d] : d.paths

  for (const item of items) {
    if (typeof item === 'string') {
      children.push(<path key={item.slice(0, 20)} d={item} />)
    } else {
      const { tag, ...attrs } = item
      const Tag = tag
      children.push(<Tag key={JSON.stringify(attrs)} {...attrs} />)
    }
  }

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"
      fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
      {...props}>
      {children}
    </svg>
  )
}

/* Named exports for tree-shaking clarity */
export const Icon = renderIcon

export const categoryIcons = {
  culture: 'landmark',
  food: 'utensils',
  nature: 'treePine',
  shopping: 'shoppingBag',
  entertainment: 'ticket',
  adventure: 'mountain',
  relaxation: 'sparkles',
  transport: 'arrowRight',
}

export function getCategoryIcon(category) {
  return <Icon name={categoryIcons[category] || 'mapPin'} />
}
