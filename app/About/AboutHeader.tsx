import React, { FC } from 'react'

import { useAtomValue } from 'jotai'
import { LocaleAtom } from 'state'

import { Colored } from 'components'

const AboutHeader: FC = () => {
    const Locale = useAtomValue(LocaleAtom).About.header

    return (
        <header
            className='about-header'
            style={{
                backgroundImage: `
    linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url(/static/image/contact-header.jpg)`,
            }}
        >
            <div className='header-text title_hero'>
                <Colored {...Locale} />
            </div>
        </header>
    )
}

export default AboutHeader
